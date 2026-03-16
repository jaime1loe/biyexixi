@echo off
chcp 65001 >nul
echo ========================================
echo    登录背景图片配置工具
echo ========================================
echo.

set "SOURCE=C:\Users\19719\Desktop\2026毕业实习\mypro\login.png"
set "DEST=C:\Users\19719\Desktop\2026毕业实习\mypro\frontend\public\login.png"

echo 正在复制图片...
echo 源文件: %SOURCE%
echo 目标位置: %DEST%
echo.

if not exist "%SOURCE%" (
    echo [错误] 源文件不存在！
    echo 请确认以下路径存在: %SOURCE%
    pause
    exit /b 1
)

if not exist "C:\Users\19719\Desktop\2026毕业实习\mypro\frontend\public\" (
    echo [错误] 目标目录不存在，正在创建...
    mkdir "C:\Users\19719\Desktop\2026毕业实习\mypro\frontend\public\"
)

copy /Y "%SOURCE%" "%DEST%" >nul

if %errorlevel% equ 0 (
    echo [成功] 图片已成功复制！
    echo.
    echo 文件位置: %DEST%
    echo.
    echo 现在可以启动前端开发服务器查看效果了。
) else (
    echo [失败] 复制文件时出错！
    echo 错误代码: %errorlevel%
)

echo.
pause