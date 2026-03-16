@echo off
echo ========================================
echo 清理项目不必要的文件
echo ========================================
echo.

echo [1/8] 清理 Python 缓存文件 (.pyc)...
cd backend
del /s /q *.pyc 2>nul
cd ..
echo 完成.

echo [2/8] 清理 Python 虚拟环境 (venv) 中的临时文件...
if exist "backend\venv" (
    echo 警告: 检测到虚拟环境目录
    echo 虚拟环境占用较大空间，如需重新安装依赖可删除 backend\venv 文件夹
)
echo.

echo [3/8] 清理前端 node_modules...
if exist "frontend\node_modules" (
    echo node_modules 占用大量空间，如需重新安装依赖可删除 frontend\node_modules 文件夹
    echo 删除后运行: cd frontend ^&^& npm install
)
echo.

echo [4/8] 清理前端 dist 构建目录...
if exist "frontend\dist" (
    rmdir /s /q "frontend\dist"
    echo 已删除 frontend\dist
)
echo.

echo [5/8] 清理 Vite 缓存...
if exist "frontend\node_modules\.vite" (
    rmdir /s /q "frontend\node_modules\.vite"
    echo 已删除 Vite 缓存
)
echo.

echo [6/8] 清理根目录临时测试脚本...
del /q "add_status_column.py" 2>nul
del /q "check_database_connection.py" 2>nul
del /q "check_db.py" 2>nul
del /q "check_system.ps1" 2>nul
del /q "clear_vite_cache.bat" 2>nul
del /q "create_notification_table.sql" 2>nul
del /q "create_tables.py" 2>nul
del /q "diagnose_auth_issue.py" 2>nul
del /q "diagnose.bat" 2>nul
del /q "fix_database.bat" 2>nul
del /q "fix_database.py" 2>nul
del /q "fix_knowledge_table.py" 2>nul
del /q "fix_qa_history.py" 2>nul
del /q "generate_notifications.py" 2>nul
del /q "generate_sample_data.py" 2>nul
del /q "import_data.py" 2>nul
del /q "init_database_tables.py" 2>nul
del /q "install_crawler_deps.py" 2>nul
del /q "plan.md" 2>nul
del /q "quick_check.bat" 2>nul
del /q "run_migration.py" 2>nul
del /q "test_issue.py" 2>nul
del /q "test_mysql.py" 2>nul
del /q "test_server.py" 2>nul
del /q "update_knowledge_status.py" 2>nul
del /q "update_notifications_table.py" 2>nul
echo 已删除临时脚本
echo.

echo [7/8] 清理 backend 目录临时脚本...
cd backend
del /q "add_ask_count_field.py" 2>nul
del /q "add_knowledge_review_fields.py" 2>nul
del /q "BACKEND_STATUS.md" 2>nul
del /q "check_all_tables.py" 2>nul
del /q "check_database.py" 2>nul
del /q "check_table_structure.py" 2>nul
del /q "check_tables.py" 2>nul
del /q "clean_pip.bat" 2>nul
del /q "create_db.py" 2>nul
del /q "DATABASE_INIT.md" 2>nul
del /q "debug_start.py" 2>nul
del /q "diagnose_database_issue.py" 2>nul
del /q "fix_users_table.py" 2>nul
del /q "full_test.py" 2>nul
del /q "init_data.py" 2>nul
del /q "init_database.sql" 2>nul
del /q "init_db_with_pwd.bat" 2>nul
del /q "init_db.bat" 2>nul
del /q "install_deps.bat" 2>nul
del /q "migrate_all_tables.py" 2>nul
del /q "migrate_database.py" 2>nul
del /q "quick_check.py" 2>nul
del /q "quick_init_db.py" 2>nul
del /q "reset_data_auto.py" 2>nul
del /q "reset_data.py" 2>nul
del /q "run_server.py" 2>nul
del /q "sale.sql" 2>nul
del /q "start_qa.bat" 2>nul
del /q "start_server.py" 2>nul
del /q "start.bat" 2>nul
del /q "test_auth_api.py" 2>nul
del /q "test_complete_system.py" 2>nul
del /q "test_config.py" 2>nul
del /q "test_db_connection.py" 2>nul
del /q "test_exceptions.py" 2>nul
del /q "test_imports.py" 2>nul
del /q "test_question_api.py" 2>nul
del /q "test_register.py" 2>nul
del /q "requirements-ai.txt" 2>nul
del /q "requirements-core.txt" 2>nul
del /q "pyrightconfig.json" 2>nul
cd ..
echo 已删除 backend 临时脚本
echo.

echo [8/8] 清理前端文档...
cd frontend
del /q "空白页面诊断与修复.md" 2>nul
del /q "缩放功能测试说明.md" 2>nul
del /q "系统设置功能说明.md" 2>nul
del /q "详细启动步骤.md" 2>nul
del /q "项目启动说明.md" 2>nul
del /q "start_frontend.bat" 2>nul
del /q "运行前端.bat" 2>nul
cd ..
echo 已删除前端临时文档
echo.

echo ========================================
echo 清理完成！
echo ========================================
echo.
echo 保留的文档:
echo   - README.md
echo   - 本周项目开发进度报告.md
echo   - 管理员后台去除首页功能.md
echo   - 后端功能实现报告.md
echo   - 基于大模型智能体的高校知识库在线答疑系统项目需求调研报告.md
echo.
echo 保留的启动脚本:
echo   - 完整启动系统.bat
echo   - 启动后端.bat
echo   - 重启前端服务.bat
echo.
echo 如需进一步释放空间，可手动删除:
echo   1. backend\venv (虚拟环境，约 500MB+)
echo   2. frontend\node_modules (依赖包，约 500MB+)
echo.
pause
