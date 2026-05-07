@echo off
REM AI热搜雷达 - Windows启动脚本

echo ==========================================
echo   AI 热搜雷达 - 启动中...
echo ==========================================

REM 检查Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装
    pause
    exit /b 1
)

REM 安装依赖
echo 检查依赖...
pip install -q fastapi uvicorn httpx beautifulsoup4 apscheduler 2>nul

REM 生成SSL证书
if not exist "certs\cert.pem" (
    echo 生成SSL证书...
    mkdir certs 2>nul
    openssl req -x509 -newkey rsa:2048 -keyout certs\key.pem -out certs\cert.pem -days 365 -nodes -subj "/CN=localhost" 2>nul
)

echo.
echo ==========================================
echo   启动成功！
echo ==========================================
echo.
echo   访问地址: https://127.0.0.1:8443
echo.
echo   手机安装步骤:
echo   1. 手机和电脑连同一WiFi
echo   2. 手机浏览器打开 https://你的电脑IP:8443
echo   3. 忽略证书警告
echo   4. iOS: 分享 - 添加到主屏幕
echo   5. Android: 菜单 - 添加到主屏幕
echo.
echo   按 Ctrl+C 停止服务
echo ==========================================

python run_https.py
pause
