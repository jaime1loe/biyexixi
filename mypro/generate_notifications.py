#!/usr/bin/env python3
"""
生成武科大风格详细通知数据的脚本
"""
import sys
import os
from datetime import datetime, timedelta

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.database import SessionLocal
    from app.models import Notification
    
    print("正在生成武科大风格详细通知数据...")
    
    # 武科大风格详细通知数据（基于2026年3月官网内容）
    wust_notifications = [
        {
            "title": "关于武汉科技大学体育场馆开放时间的通知",
            "content": "根据学校工作安排，现将体育场馆开放时间进行调整，请各学院通知师生合理安排体育活动时间。",
            "detail_content": """
<h3>关于武汉科技大学体育场馆开放时间的通知</h3>
<p><strong>各学院、各位师生：</strong></p>

<p>为更好地满足师生体育锻炼需求，根据学校工作安排，现将体育场馆开放时间通知如下：</p>

<h4>一、开放时间安排</h4>
<ul>
<li><strong>黄家湖校区体育馆：</strong>周一至周五 8:00-22:00，周末 8:00-20:00</li>
<li><strong>青山校区体育馆：</strong>周一至周五 8:00-21:00，周末 8:00-18:00</li>
<li><strong>室外运动场：</strong>每日6:00-22:00开放</li>
<li><strong>游泳馆：</strong>夏季（6月-9月）开放，具体时间另行通知</li>
</ul>

<h4>二、注意事项</h4>
<ol>
<li>请师生遵守场馆管理规定，文明使用体育设施</li>
<li>团体活动需提前预约，预约电话：027-68862555</li>
<li>如遇学校重大活动，场馆开放时间将临时调整</li>
<li>寒暑假期间开放时间另行通知</li>
</ol>

<h4>三、联系方式</h4>
<p>体育学院办公室：027-68862566<br>
场馆管理中心：027-68862567</p>

<p><strong>武汉科技大学体育学院</strong><br>
2026年3月9日</p>
""",
            "category": "校园服务",
            "is_important": 0,
            "publisher": "武汉科技大学体育学院"
        },
        {
            "title": "2025~2026学年第二学期第一周学校工作安排",
            "content": "2025~2026学年第二学期第一周学校工作安排已发布，请各单位按照安排做好开学准备工作。",
            "detail_content": """
<h3>2025~2026学年第二学期第一周学校工作安排</h3>
<p><strong>全校各单位：</strong></p>

<p>为确保新学期各项工作有序开展，现将2025~2026学年第二学期第一周学校工作安排通知如下：</p>

<h4>一、时间安排</h4>
<ul>
<li><strong>教职工返校：</strong>2026年3月2日（星期一）</li>
<li><strong>学生报到注册：</strong>2026年3月2日-3月3日</li>
<li><strong>正式上课：</strong>2026年3月4日（星期三）</li>
<li><strong>开学典礼：</strong>2026年3月4日上午8:30，黄家湖校区体育馆</li>
</ul>

<h4>二、主要工作</h4>
<ol>
<li><strong>教学准备工作：</strong>各教学单位做好课程安排、教材发放、教室检查等工作</li>
<li><strong>学生工作：</strong>各学院做好学生报到注册、宿舍安排、安全教育等工作</li>
<li><strong>后勤保障：</strong>后勤部门做好校园环境整治、餐饮服务、水电保障等工作</li>
<li><strong>安全保卫：</strong>保卫处加强校园安全管理，确保开学期间校园秩序</li>
</ol>

<h4>三、会议要求</h4>
<ol>
<li><strong>中层干部会议：</strong>3月2日上午9:00，行政楼一楼会议室</li>
<li><strong>教学工作例会：</strong>3月3日下午2:30，教务处会议室</li>
<li><strong>学生工作例会：</strong>3月3日下午4:00，学生工作处会议室</li>
</ol>

<p><strong>武汉科技大学办公室</strong><br>
2026年3月9日</p>
""",
            "category": "学校工作",
            "is_important": 1,
            "publisher": "武汉科技大学办公室"
        },
        {
            "title": "关于开展2026年度国家有关人才计划教学名师项目申报推荐工作的紧急通知",
            "content": "根据上级通知要求，现开展2026年度国家有关人才计划教学名师项目申报推荐工作，请符合条件的教师积极申报。",
            "detail_content": """
<h3>关于开展2026年度国家有关人才计划教学名师项目申报推荐工作的紧急通知</h3>
<p><strong>各学院、各单位：</strong></p>

<p>根据《教育部办公厅关于开展2026年度国家有关人才计划教学名师项目申报推荐工作的通知》要求，现就我校申报推荐工作有关事项通知如下：</p>

<h4>一、申报条件</h4>
<ol>
<li>忠诚于党和人民的教育事业，全面贯彻党的教育方针</li>
<li>长期从事一线教学工作，教学成果显著</li>
<li>师德高尚，关爱学生，教书育人成果突出</li>
<li>在教育教学改革中取得创新性成果</li>
<li>具有高级专业技术职务，年龄一般不超过55周岁</li>
</ol>

<h4>二、申报材料</h4>
<ul>
<li>《国家有关人才计划教学名师项目申报书》</li>
<li>个人主要业绩材料及相关证明材料</li>
<li>教学成果、科研项目等证明材料</li>
<li>所在单位推荐意见</li>
</ul>

<h4>三、时间安排</h4>
<ol>
<li><strong>个人申报：</strong>2026年3月6日-3月10日</li>
<li><strong>学院推荐：</strong>2026年3月11日-3月13日</li>
<li><strong>学校评审：</strong>2026年3月14日-3月15日</li>
<li><strong>材料报送：</strong>2026年3月16日前</li>
</ol>

<h4>四、工作要求</h4>
<ol>
<li>各学院要高度重视，精心组织，确保推荐质量</li>
<li>严格审核申报材料，确保真实准确</li>
<li>按时报送材料，逾期不予受理</li>
</ol>

<h4>五、联系方式</h4>
<p>人事处师资科：027-68862577<br>
联系人：张老师、李老师</p>

<p><strong>武汉科技大学人事处</strong><br>
2026年3月6日</p>
""",
            "category": "人才工作",
            "is_important": 1,
            "publisher": "武汉科技大学人事处"
        },
        {
            "title": "关于开展2026年国家有关教育人才项目和青年科技人才项目申报推荐工作的通知",
            "content": "根据上级通知，现开展2026年国家有关教育人才项目和青年科技人才项目申报推荐工作，请各单位积极组织申报。",
            "detail_content": """
<h3>关于开展2026年国家有关教育人才项目和青年科技人才项目申报推荐工作的通知</h3>
<p><strong>各学院、各单位：</strong></p>

<p>根据国家有关人才计划和青年科技人才项目的申报要求，现就我校2026年度申报推荐工作有关事项通知如下：</p>

<h4>一、申报项目类别</h4>
<ol>
<li><strong>国家有关教育人才项目：</strong>面向在教学科研一线工作的优秀人才</li>
<li><strong>青年科技人才项目：</strong>面向40周岁以下的青年科技人才</li>
</ol>

<h4>二、申报条件</h4>
<ul>
<li>热爱祖国，遵纪守法，学风正派</li>
<li>在教学科研一线工作，业绩突出</li>
<li>具有博士学位或高级专业技术职务</li>
<li>青年科技人才项目申报人年龄不超过40周岁</li>
<li>无学术不端行为，无违纪违法记录</li>
</ul>

<h4>三、申报材料</h4>
<ol>
<li>《国家有关人才项目申报书》</li>
<li>个人简历及主要业绩材料</li>
<li>代表性成果证明材料</li>
<li>所在单位推荐意见</li>
<li>其他相关证明材料</li>
</ol>

<h4>四、时间安排</h4>
<ul>
<li><strong>材料准备：</strong>2026年3月6日-3月12日</li>
<li><strong>学院审核：</strong>2026年3月13日-3月15日</li>
<li><strong>学校评审：</strong>2026年3月16日-3月18日</li>
<li><strong>材料报送：</strong>2026年3月20日前</li>
</ul>

<h4>五、联系方式</h4>
<p>科研处项目管理科：027-68862588<br>
人事处师资科：027-68862577</p>

<p><strong>武汉科技大学科研处、人事处</strong><br>
2026年3月6日</p>
""",
            "category": "科研工作",
            "is_important": 1,
            "publisher": "武汉科技大学科研处、人事处"
        },
        {
            "title": "2026年固定资产盘点实施方案",
            "content": "根据学校资产管理要求，现制定2026年固定资产盘点实施方案，请各单位认真组织实施。",
            "detail_content": """
<h3>2026年固定资产盘点实施方案</h3>
<p><strong>全校各单位：</strong></p>

<p>为进一步加强固定资产管理，摸清学校资产底数，提高资产使用效益，根据《武汉科技大学固定资产管理办法》要求，现制定2026年固定资产盘点实施方案如下：</p>

<h4>一、盘点范围</h4>
<ol>
<li>学校所有固定资产，包括房屋建筑物、仪器设备、家具用具等</li>
<li>各二级单位、实验室、办公室、教室等场所的资产</li>
<li>截止2026年3月1日前的所有在账资产</li>
</ol>

<h4>二、盘点时间</h4>
<ul>
<li><strong>准备阶段：</strong>2026年3月6日-3月10日</li>
<li><strong>实施阶段：</strong>2026年3月11日-3月25日</li>
<li><strong>汇总阶段：</strong>2026年3月26日-3月31日</li>
</ul>

<h4>三、组织实施</h4>
<ol>
<li><strong>学校层面：</strong>成立固定资产盘点工作领导小组</li>
<li><strong>单位层面：</strong>各二级单位成立盘点工作小组</li>
<li><strong>人员配备：</strong>各单位指定专人负责盘点工作</li>
</ol>

<h4>四、工作要求</h4>
<ul>
<li>各单位要高度重视，精心组织，确保盘点质量</li>
<li>盘点数据要真实准确，不得虚报、瞒报、漏报</li>
<li>对盘点中发现的问题要及时整改</li>
<li>按时完成盘点任务，及时报送盘点结果</li>
</ul>

<h4>五、联系方式</h4>
<p>资产管理处：027-68862599<br>
联系人：王老师、刘老师</p>

<p><strong>武汉科技大学资产管理处</strong><br>
2026年3月6日</p>
""",
            "category": "资产管理",
            "is_important": 1,
            "publisher": "武汉科技大学资产管理处"
        },
        {
            "title": "关于开展校外使用仪器设备清查工作的通知",
            "content": "为加强仪器设备管理，现开展校外使用仪器设备清查工作，请相关单位认真组织自查。",
            "detail_content": """
<h3>关于开展校外使用仪器设备清查工作的通知</h3>
<p><strong>各相关单位：</strong></p>

<p>为进一步加强仪器设备管理，防止国有资产流失，根据《武汉科技大学仪器设备管理办法》要求，现就开展校外使用仪器设备清查工作通知如下：</p>

<h4>一、清查范围</h4>
<ol>
<li>所有校外使用的学校仪器设备</li>
<li>合作单位借用、租赁的仪器设备</li>
<li>校外科研项目使用的仪器设备</li>
<li>其他校外使用的学校资产</li>
</ol>

<h4>二、清查内容</h4>
<ul>
<li>仪器设备的使用单位、使用人、使用地点</li>
<li>仪器设备的借用、租赁协议或合同</li>
<li>仪器设备的使用状况、维护保养情况</li>
<li>是否存在违规使用、流失风险</li>
</ul>

<h4>三、时间安排</h4>
<ol>
<li><strong>自查阶段：</strong>2026年3月6日-3月15日</li>
<li><strong>检查阶段：</strong>2026年3月16日-3月20日</li>
<li><strong>整改阶段：</strong>2026年3月21日-3月25日</li>
<li><strong>总结阶段：</strong>2026年3月26日-3月31日</li>
</ol>

<h4>四、工作要求</h4>
<ol>
<li>各相关单位要高度重视，认真组织自查</li>
<li>对清查发现的问题要及时整改</li>
<li>建立健全校外使用仪器设备管理制度</li>
<li>加强日常监管，防止国有资产流失</li>
</ol>

<h4>五、联系方式</h4>
<p>实验室与设备管理处：027-68862600<br>
联系人：陈老师、赵老师</p>

<p><strong>武汉科技大学实验室与设备管理处</strong><br>
2026年3月6日</p>
""",
            "category": "设备管理",
            "is_important": 1,
            "publisher": "武汉科技大学实验室与设备管理处"
        },
        {
            "title": "武汉科技大学2026年3月理论学习安排",
            "content": "根据《武汉科技大学党委理论学习中心组学习实施细则》有关规定，现就2026年3月理论学习安排如下。",
            "detail_content": """
<h3>武汉科技大学2026年3月理论学习安排</h3>
<p><strong>全校各单位：</strong></p>

<p>根据《武汉科技大学党委理论学习中心组学习实施细则》(武科大党〔2018〕31 号)有关规定，现就2026年3月理论学习安排如下：</p>

<h4>一、学习时间</h4>
<p>2026年3月</p>

<h4>二、学习内容</h4>
<ol>
<li><strong>习近平总书记近期重要讲话重要指示精神</strong><br>
重点学习习近平总书记在2月27日中共中央政治局会议上的重要讲话精神，深刻领会党中央关于当前形势的分析判断和重大决策部署。</li>

<li><strong>全国两会精神</strong><br>
认真学习2026年全国两会精神，特别是政府工作报告中关于教育、科技、人才工作的重要论述。</li>

<li><strong>高等教育改革发展政策</strong><br>
深入学习教育部关于高等教育改革发展的最新政策文件，结合学校实际研究贯彻落实措施。</li>

<li><strong>全面从严治党要求</strong><br>
学习党中央关于全面从严治党的最新要求，加强党风廉政建设和反腐败工作。</li>
</ol>

<h4>三、学习方式</h4>
<ul>
<li>个人自学与集中学习相结合</li>
<li>理论学习与工作实际相结合</li>
<li>专家辅导与交流研讨相结合</li>
<li>线上学习与线下学习相结合</li>
</ul>

<h4>四、学习要求</h4>
<ol>
<li>各单位要高度重视理论学习，认真组织落实</li>
<li>领导干部要带头学习，发挥示范作用</li>
<li>要注重学习效果，做到学以致用</li>
<li>要及时总结学习情况，按时报送学习材料</li>
</ol>

<h4>五、学习资料</h4>
<p>学习资料将通过学校党委宣传部网站和学习强国平台发布，请各单位及时下载学习。</p>

<p><strong>武汉科技大学党委宣传部</strong><br>
2026年3月5日</p>
""",
            "category": "理论学习",
            "is_important": 1,
            "publisher": "武汉科技大学党委宣传部"
        }
    ]
    
    db = SessionLocal()
    try:
        # 检查是否已有通知数据
        existing_count = db.query(Notification).count()
        
        # 删除现有数据（如果需要重新生成）
        if existing_count > 0:
            print(f"删除现有 {existing_count} 条通知数据...")
            db.query(Notification).delete()
            db.commit()
        
        # 插入武科大风格详细数据
        for i, notification_data in enumerate(wust_notifications):
            # 设置不同的创建时间
            created_at = datetime.now() - timedelta(days=i*2)
            
            notification = Notification(
                title=notification_data["title"],
                content=notification_data["content"],
                detail_content=notification_data["detail_content"],
                category=notification_data["category"],
                is_important=notification_data["is_important"],
                publisher=notification_data.get("publisher", "武汉科技大学"),
                created_at=created_at,
                views=0
            )
            db.add(notification)
        
        db.commit()
        print(f"成功插入 {len(wust_notifications)} 条武科大风格详细通知数据")
        
        # 显示通知数据详情
        notifications = db.query(Notification).order_by(Notification.created_at.desc()).all()
        print(f"\n当前通知列表（共 {len(notifications)} 条）:")
        print("=" * 80)
        for notif in notifications:
            importance = "【重要】" if notif.is_important == 1 else "【普通】"
            publisher = notif.publisher or "武汉科技大学"
            print(f"{importance} [{notif.category}] {notif.title}")
            print(f"   发布单位: {publisher}")
            print(f"   发布时间: {notif.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"   摘要: {notif.content}")
            print("-" * 80)
        
        # 显示第一条通知的详细内容示例
        if notifications:
            first_notif = notifications[0]
            print(f"\n第一条通知的详细内容示例:")
            print("=" * 80)
            print(first_notif.detail_content)
            print("=" * 80)
            
    finally:
        db.close()
    
    print("\n武科大风格通知数据生成完成！")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()