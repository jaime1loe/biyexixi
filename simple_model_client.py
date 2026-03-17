"""
模型客户端 - 基于 Ollama 的智能问答
使用 Ollama 本地大模型 + RAG 知识库增强
"""
import asyncio
import logging
import json
from typing import Optional, List, Dict
import aiohttp

from config import settings

logger = logging.getLogger(__name__)


class QAResult:
    """问答结果"""
    def __init__(self, answer: str, suggested_questions: List[str] = None):
        self.answer = answer
        self.suggested_questions = suggested_questions or []


class SimpleModelClient:
    """Ollama 模型客户端 - 支持本地大模型 + 知识库增强"""

    def __init__(self):
        self.model_name = settings.OLLAMA_MODEL
        self.base_url = settings.OLLAMA_BASE_URL
        self.timeout = settings.OLLAMA_TIMEOUT
        self._health_check_passed = False

        # 知识库 - 用于 RAG 增强
        self.knowledge_base = {
            "选课": "网上选课流程：\n1. 登录教务系统\n2. 进入选课中心\n3. 选择课程\n4. 提交确认\n\n注意：选课时间通常在每学期开始前一周，请关注教务处通知。",
            "成绩": "查询成绩方式：\n1. 登录教务系统\n2. 进入【成绩查询】模块\n3. 选择学期\n4. 查看所有课程成绩\n\n如有疑问，可联系教务处。",
            "教务": "教务处主要职能：\n- 课程安排与选课管理\n- 成绩管理\n- 学籍管理\n- 毕业审核\n\n办公地点：行政楼2楼",
            "学籍": "学籍相关业务包括：\n1. 学籍注册\n2. 学籍异动（休学、复学、转专业）\n3. 毕业资格审核\n\n办理地点：教务处学籍管理科",
            "奖学金": "奖学金评定标准：\n一等奖学金：成绩前10%，5000元/年\n二等奖学金：成绩前20%，3000元/年\n三等奖学金：成绩前30%，1500元/年\n\n申请时间：每学年第一学期初",
            "助学金": "助学金申请：\n1. 家庭经济困难学生可申请\n2. 需提交《家庭经济困难学生认定申请表》\n3. 经班级、学院、学校三级认定\n\n具体金额根据困难等级确定",
            "图书馆": "图书馆服务：\n1. 图书借阅\n2. 座位预约（微信小程序）\n3. 电子资源访问\n4. 研修室预约\n\n开放时间：周一至周五 8:00-22:00\n周六周日 9:00-21:00",
            "借书": "图书借阅规则：\n1. 借阅数量：本科生5册，研究生10册\n2. 借阅期限：30天，可续借1次\n3. 逾期费用：0.1元/册/天\n\n请使用一卡通借阅",
            "一卡通": "校园一卡通功能：\n1. 食堂消费\n2. 图书馆借书\n3. 门禁出入\n4. 超市购物\n\n充值方式：微信、支付宝自助充值",
            "宿舍": "宿舍管理规定：\n1. 晚归时间：23:00\n2. 禁止使用大功率电器（热得快、电饭煲等）\n3. 保持卫生整洁\n4. 禁止校外人员留宿\n\n如有特殊情况需提前请假",
            "食堂": "学校食堂分布：\n1. 第一食堂：主教学楼旁\n2. 第二食堂：图书馆对面\n3. 第三食堂：宿舍区\n\n营业时间：6:30-21:00",
            "毕业": "毕业流程：\n1. 毕业论文/设计\n2. 毕业实习\n3. 毕业资格审核\n4. 毕业典礼\n\n具体时间安排请关注教务处通知",
            "实习": "毕业实习说明：\n1. 实习时间：最后一学期\n2. 实习时长：2-3个月\n3. 需要提交：实习报告、实习鉴定表\n4. 实习学分：一般4学分",
            "论文": "毕业论文要求：\n1. 字数：不少于8000字\n2. 查重率：一般要求低于15%\n3. 格式：按学校模板要求\n4. 答辩：通过后方可毕业",
            "考试": "考试安排：\n1. 期末考试：每学期末\n2. 补考：开学初\n3. 四六级考试：每年6月、12月\n\n请提前关注教务处通知",
            "四六级": "英语四六级考试：\n1. 报名时间：每年3月、9月\n2. 考试时间：6月、12月\n3. 成绩查询：考后60个工作日\n\n报名资格：本科在校生",
            "登录": "登录说明：\n1. 学生账号：学号\n2. 初始密码：123456\n3. 首次登录建议修改密码\n\n如忘记密码，可联系辅导员重置",
        }

    def _retrieve_knowledge(self, question: str) -> str:
        """从知识库中检索相关内容"""
        question_lower = question.lower()
        relevant_info = []

        for key, value in self.knowledge_base.items():
            if key in question_lower:
                relevant_info.append(f"【{key}】{value}")

        if relevant_info:
            return "\n\n".join(relevant_info)
        return ""

    def _build_prompt(self, question: str, history: List[Dict[str, str]] = None) -> str:
        """构建提示词，包含知识库上下文和历史对话"""
        # 检索相关知识（仅对校园相关问题）
        question_lower = question.lower()
        is_campus_question = any(kw in question_lower for kw in ["选课", "成绩", "图书馆", "奖学金", "宿舍", "毕业", "实习", "论文", "考试", "教务", "学籍", "一卡通", "食堂", "登录", "四六级", "助学金"])
        
        context = ""
        if is_campus_question:
            context = self._retrieve_knowledge(question)

        # 构建系统提示 - 更具聊天性质
        system_prompt = """你是一个温暖、有趣的校园智能问答助手。你不仅能回答校园问题，还能像朋友一样和学生聊天。

主要能力：
1. 校园相关问题：选课、成绩、图书馆、奖学金、宿舍、毕业、实习等
2. 日常聊天：可以夸赞用户、安慰用户、聊天解闷
3. 情绪价值：用户需要鼓励时可以给予正面反馈

回答要求：
1. 用中文回答，语气友好亲切
2. 校园问题要准确可靠，聊天问题要自然有趣
3. 如果用户表现出情绪（沮丧、开心、焦虑等），适当给予回应和安慰
4. 回答问题或聊天时，如果之前有相关对话，要结合上下文
5. 适当使用表情或语气词让对话更生动"""

        # 构建历史对话
        history_text = ""
        if history:
            history_text = "\n\n对话历史：\n"
            for msg in history[-6:]:  # 保留最近6条对话
                role = "用户" if msg.get("role") == "user" else "助手"
                history_text += f"{role}：{msg.get('content', '')}\n"

        if context:
            prompt = f"""{system_prompt}

【校园知识库】
{context}
{history_text}
用户问题：{question}

请根据以上信息回答，如果是聊天问题就轻松回复，如果是校园问题就专业回答。"""
        else:
            prompt = f"""{system_prompt}
{history_text}
用户问题：{question}

请根据对话上下文和用户需求回答。"""

        return prompt

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        history: List[Dict[str, str]] = None
    ) -> QAResult:
        """生成回答 - 使用 Ollama，返回回答和引导问题"""
        try:
            # 保存原始问题用于后续处理
            original_question = prompt
            # 检查是否是简单对话
            question_lower = prompt.lower().strip()
            
            logger.info(f"AI服务收到问题: {original_question[:50]}...")
            logger.info(f"Ollama配置: URL={self.base_url}, Model={self.model_name}, Timeout={self.timeout}")

            # 获取上一条AI回答（用于重新生成）
            last_assistant_answer = ""
            if history:
                for msg in reversed(history):
                    if msg.get("role") == "assistant":
                        last_assistant_answer = msg.get("content", "")
                        break

            # 重新生成回答
            if any(word in question_lower for word in ["重新生成", "换一个", "不好", "不满意", "重新回答", "换个说法", "再试一次"]):
                if last_assistant_answer:
                    # 重新生成时使用更高的temperature
                    return await self._regenerate_answer(original_question, last_assistant_answer, history, temperature=0.9)
                else:
                    # 没有上一条回答，正常生成
                    pass

            # 问候类问题
            if any(word in question_lower for word in ["你好", "hello", "hi", "您好", "在吗", "在嘛"]):
                return QAResult(
                    answer="你好呀！很高兴见到你～有什么我可以帮你的吗？无论是学习上的问题还是想聊聊天都可以问我哦！😊",
                    suggested_questions=["如何选课？", "图书馆在哪里？", "今天心情好吗？"]
                )

            # 感谢类问题
            if any(word in question_lower for word in ["谢谢", "thank", "thanks", "感谢", "谢啦", "谢谢你"]):
                return QAResult(
                    answer="不客气！能帮到你我也很开心～有问题随时来找我哦！🌟",
                    suggested_questions=["如何查询成绩？", "图书馆开放时间？", "今天怎么样？"]
                )

            # 再见类问题
            if any(word in question_lower for word in ["再见", "bye", "拜拜", "走了", "去忙"]):
                return QAResult(
                    answer="再见！有空再来找我聊天哦，祝你今天开心！👋",
                    suggested_questions=[]
                )

            # 夸夸/鼓励请求
            if any(word in question_lower for word in ["夸我", "夸夸", "鼓励", "安慰", "给我加油", "心情不好", "不开心", "郁闷", "难过", "沮丧", "累", "压力大"]):
                return await self._generate_encouragement(original_question, history)

            # 聊天/闲谈
            if any(word in question_lower for word in ["聊聊", "聊天", "干嘛呢", "在做什么", "最近如何", "怎么样", "今天怎样", "最近怎么样"]):
                return await self._generate_chat(original_question, history)

            # 测试/调戏
            if any(word in question_lower for word in ["你是谁", "你叫什么", "你好笨", "你好聪明", "你喜欢"]):
                return await self._generate_personality_response(original_question, history)

            # 构建提示词（包含历史对话）
            full_prompt = self._build_prompt(original_question, history)

            # 构建请求
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": 0.9,
                    "max_tokens": max_tokens
                }
            }

            logger.info(f"调用 Ollama: model={self.model_name}, prompt={original_question[:50]}...")

            # 调用 Ollama 生成回答
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Ollama原始返回: {result}")
                        answer = result.get("response", "生成失败，请重试").strip()
                        logger.info(f"提取的回答: {answer[:100] if answer else '空'}")
                    else:
                        error_text = await response.text()
                        logger.error(f"Ollama API 错误: {response.status} - {error_text}")
                        return QAResult(
                            answer=f"抱歉，AI服务暂时不可用 (错误码: {response.status})。请稍后重试。",
                            suggested_questions=[]
                        )

            # 直接使用默认引导问题，加快响应速度
            suggested_questions = self._get_default_suggested_questions(original_question)

            return QAResult(answer=answer, suggested_questions=suggested_questions)

        except asyncio.TimeoutError:
            logger.error("Ollama 请求超时")
            return QAResult(answer="抱歉，AI响应超时，请稍后重试。", suggested_questions=[])
        except aiohttp.ClientError as e:
            logger.error(f"连接 Ollama 失败: {e}")
            return QAResult(answer="抱歉，无法连接到AI服务。请确保Ollama正在运行。", suggested_questions=[])
        except Exception as e:
            logger.error(f"生成失败: {e}")
            return QAResult(answer=f"抱歉，处理您的问题时出现了一些问题: {str(e)}", suggested_questions=[])

    async def _regenerate_answer(self, question: str, last_answer: str, history: List[Dict[str, str]] = None, temperature: float = 0.9) -> QAResult:
        """重新生成回答"""
        try:
            # 构建重新生成的提示
            prompt = f"""用户对之前的回答不满意，要求重新回答。

之前的回答：
{last_answer}

用户问题：{question}

请重新回答这个问题，换一种说法，让回答更加完善、更加符合用户需求。
回答要更详细、更有帮助，如果之前有遗漏的信息请补充上。"""

            # 添加历史上下文
            if history:
                history_text = "\n对话历史：\n"
                for msg in history[:-1]:  # 排除上一条助手回答
                    role = "用户" if msg.get("role") == "user" else "助手"
                    history_text += f"{role}：{msg.get('content', '')}\n"
                prompt = f"{prompt}\n{history_text}"

            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": 0.9,
                    "max_tokens": 600
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        answer = result.get("response", "生成失败，请重试").strip()
                    else:
                        answer = "抱歉，重新生成失败了。请稍后再试～"

            suggested_questions = self._get_default_suggested_questions(question)
            return QAResult(answer=answer, suggested_questions=suggested_questions)

        except Exception as e:
            logger.error(f"重新生成失败: {e}")
            return QAResult(answer="抱歉，重新生成失败了。没关系，我们可以换个话题聊聊～", suggested_questions=[])

    async def _generate_encouragement(self, question: str, history: List[Dict[str, str]] = None) -> QAResult:
        """生成鼓励/安慰回复"""
        try:
            question_lower = question.lower()
            
            # 获取用户之前可能提到的不开心原因
            context = ""
            if history:
                for msg in history[-3:]:
                    if msg.get("role") == "user":
                        context = msg.get("content", "")[-100:]

            prompt = f"""用户需要鼓励或安慰。请给出温暖、正面的回复。

用户的原话：{question}
上下文：{context}

要求：
1. 语气温暖真诚，像朋友一样关心用户
2. 适当安慰鼓励，让用户感受到被理解
3. 可以适当用表情符号
4. 简短但有力量，50字以内
5. 如果用户提到具体烦恼，给出针对性安慰"""

            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "max_tokens": 200
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        answer = result.get("response", "哎呀，不管发生什么，你都很棒！相信自己，一切都会好起来的！💪").strip()
                    else:
                        answer = "不管怎么样，你都很优秀！相信自己，继续加油！🌟"

            return QAResult(answer=answer, suggested_questions=["想聊聊别的吗？", "有什么我可以帮你的？", "今天想聊些什么？"])

        except Exception as e:
            logger.error(f"生成鼓励回复失败: {e}")
            return QAResult(answer="你很棒的！不管发生什么，都要相信自己！💪加油！", suggested_questions=[])

    async def _generate_chat(self, question: str, history: List[Dict[str, str]] = None) -> QAResult:
        """生成聊天回复"""
        try:
            # 获取对话上下文
            context = ""
            if history:
                for msg in history[-4:]:
                    role = "用户" if msg.get("role") == "user" else "我"
                    context += f"{role}：{msg.get('content', '')}\n"

            prompt = f"""用户想聊天。请给出轻松有趣的回复。

对话历史：
{context}

用户最新消息：{question}

要求：
1. 轻松自然，像朋友聊天
2. 可以适当用表情
3. 简短有趣，50字以内
4. 可以反问或找话题继续聊
5. 如果用户问你在干嘛，回答得有趣一些"""

            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "max_tokens": 150
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        answer = result.get("response", "哈哈，我挺好的呀！随时待命陪你聊天～有什么想聊的吗？").strip()
                    else:
                        answer = "我挺好的，陪你聊天很开心！你呢，今天怎么样？"

            return QAResult(answer=answer, suggested_questions=["有什么校园问题吗？", "今天心情好吗？", "聊聊别的？"])

        except Exception as e:
            logger.error(f"生成聊天回复失败: {e}")
            return QAResult(answer="哈哈，陪你聊天很开心！有什么想问或想聊的吗？😊", suggested_questions=[])

    async def _generate_personality_response(self, question: str, history: List[Dict[str, str]] = None) -> QAResult:
        """生成关于AI自身的回复"""
        answers = [
            "我是一个校园智能问答助手呀！不过也是个可以聊天的小伙伴～有什么想问我的吗？😊",
            "我是你的校园小助手呀！不仅能回答学习问题，还能陪你聊聊天～今天有什么想聊的吗？🌟",
            "哈喽！我是校园问答AI，专门帮助同学们解决问题。当然，无聊的时候也可以找我聊聊天啦～😄"
        ]
        import random
        answer = random.choice(answers)
        return QAResult(answer=answer, suggested_questions=["你能做什么？", "图书馆在哪？", "今天怎么样？"])

    async def _generate_suggested_questions(self, original_question: str, answer: str) -> List[str]:
        """生成引导问题"""
        try:
            prompt = f"""基于用户问题"{original_question}"和回答，生成3个用户可能想要进一步了解的深入问题。

要求：
1. 问题要简短，不超过20个字
2. 问题要与原问题相关，是进一步深入的问题
3. 返回格式：只需返回3个问题，每行一个，不要有其他内容

用户问题：{original_question}
回答：{answer[:200]}"""

            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "max_tokens": 150
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        suggested_text = result.get("response", "").strip()

                        # 解析问题
                        questions = []
                        for line in suggested_text.split('\n'):
                            line = line.strip()
                            # 去除数字前缀、点号等
                            line = line.lstrip('0123456789.）) ').strip()
                            if line and len(line) <= 25:
                                questions.append(line)

                        # 确保有3个问题
                        default_questions = self._get_default_suggested_questions(original_question)
                        while len(questions) < 3:
                            for q in default_questions:
                                if q not in questions:
                                    questions.append(q)
                                    if len(questions) >= 3:
                                        break

                        return questions[:3]
                    else:
                        return self._get_default_suggested_questions(original_question)

        except Exception as e:
            logger.warning(f"生成引导问题失败: {e}")
            return self._get_default_suggested_questions(original_question)

    def _get_default_suggested_questions(self, question: str) -> List[str]:
        """获取默认引导问题"""
        question_lower = question.lower()

        if "选课" in question_lower:
            return ["如何查询选课结果？", "选课时间是什么时候？", "可以跨专业选课吗？"]
        elif "成绩" in question_lower:
            return ["如何打印成绩单？", "成绩有异议怎么办？", "绩点怎么计算？"]
        elif "图书馆" in question_lower or "借书" in question_lower:
            return ["如何预约座位？", "图书逾期怎么办？", "如何访问电子资源？"]
        elif "奖学金" in question_lower or "助学金" in question_lower:
            return ["奖学金什么时候发放？", "国家助学金申请条件？", "奖学金评定标准是什么？"]
        elif "宿舍" in question_lower:
            return ["宿舍怎么分配？", "可以申请调换宿舍吗？", "宿舍维修怎么申请？"]
        elif "毕业" in question_lower:
            return ["毕业需要满足什么条件？", "毕业论文怎么选题？", "毕业典礼什么时候？"]
        elif "实习" in question_lower:
            return ["实习单位怎么找？", "实习报告怎么写？", "实习学分怎么算？"]
        elif "考试" in question_lower or "四六级" in question_lower:
            return ["考试不及格怎么办？", "如何申请缓考？", "四六级在哪报名？"]
        elif "一卡通" in question_lower or "校园卡" in question_lower:
            return ["一卡通怎么充值？", "卡丢了怎么办？", "密码忘记了怎么办？"]
        elif "食堂" in question_lower:
            return ["食堂开放时间？", "支持哪些支付方式？", "清真餐厅在哪里？"]
        else:
            return ["还有其他问题吗？", "需要更多帮助吗？", "想了解其他信息吗？"]

    def health_check(self) -> dict:
        """健康检查 - 测试 Ollama 连接"""
        try:
            import requests
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                self._health_check_passed = True
                return {
                    "status": "healthy",
                    "model": self.model_name,
                    "available_models": model_names,
                    "knowledge_items": len(self.knowledge_base)
                }
            else:
                return {
                    "status": "unhealthy",
                    "model": self.model_name,
                    "error": f"API返回状态码: {response.status_code}"
                }
        except Exception as e:
            logger.warning(f"Ollama 健康检查失败: {e}")
            return {
                "status": "unhealthy",
                "model": self.model_name,
                "error": str(e)
            }


# 全局模型客户端实例
simple_llm_client = SimpleModelClient()
