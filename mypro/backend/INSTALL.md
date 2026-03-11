# 安装指南

## 快速安装（推荐）

### 方式一：使用自动安装脚本

双击运行 `install_deps.bat`，脚本会自动安装所有核心依赖。

### 方式二：手动安装

```bash
cd backend
pip install fastapi uvicorn sqlalchemy pymysql pydantic pydantic-settings passlib[bcrypt] python-jose[cryptography] python-multipart aiofiles -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方式三：使用requirements文件

如果遇到哈希错误，先清理pip缓存：

```bash
pip cache purge
pip install -r requirements-core.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 安装后的步骤

### 1. 创建数据库

双击运行 `init_db_with_pwd.bat`，输入MySQL密码。

### 2. 初始化测试数据（可选）

```bash
python init_data.py
```

### 3. 启动服务

```bash
python main.py
```

或双击运行 `start.bat`。

---

## 常见问题

### 哈希校验失败

运行清理脚本：
```bash
clean_pip.bat
```

或手动清理：
```bash
pip cache purge
pip uninstall -y fastapi uvicorn sqlalchemy pymysql pydantic passlib
pip install -r requirements-core.txt
```

### 编码错误

已修复：所有 `requirements-*.txt` 文件已移除中文注释。

### 版本冲突

- 使用 `requirements-core.txt` 安装核心依赖
- 使用 `requirements-ai.txt` 安装AI依赖（后续阶段）

---

## 验证安装

运行以下命令验证：

```bash
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"
python -c "import sqlalchemy; print('SQLAlchemy:', sqlalchemy.__version__)"
python -c "import pymysql; print('PyMySQL: OK')"
```

如果都显示正常，说明安装成功！
