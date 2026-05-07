@echo off
REM AI热搜雷达 - Windows启动脚本

echo ==========================================
echo   AI 热搜雷达 - 启动中...
echo ==========================================

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装
    pause
    exit /b 1
)

echo 检查依赖...
pip install -q -r requirements.txt 2>nul

echo.
echo ==========================================
echo   启动成功！
echo ==========================================
echo.
echo   访问地址: http://127.0.0.1:8080
echo.
echo   按 Ctrl+C 停止服务
echo ==========================================

python run.py
pause
