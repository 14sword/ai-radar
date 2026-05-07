#!/bin/bash
# AI热搜雷达 - 一键启动脚本（macOS/Linux）

echo "=========================================="
echo "  AI 热搜雷达 - 启动中..."
echo "=========================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装"
    exit 1
fi

# 安装依赖
echo "检查依赖..."
pip3 install -q fastapi uvicorn httpx beautifulsoup4 apscheduler 2>/dev/null

# 生成SSL证书（如果不存在）
if [ ! -f "certs/cert.pem" ]; then
    echo "生成SSL证书..."
    mkdir -p certs
    openssl req -x509 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost" 2>/dev/null
fi

# 获取本机IP
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

echo ""
echo "=========================================="
echo "  启动成功！"
echo "=========================================="
echo ""
echo "  电脑访问: https://127.0.0.1:8443"
echo "  手机访问: https://${LOCAL_IP}:8443"
echo ""
echo "  手机安装步骤:"
echo "  1. 手机浏览器打开上面的手机访问地址"
echo "  2. 忽略证书警告（自签名证书）"
echo "  3. iOS: 点分享按钮 → 添加到主屏幕"
echo "  4. Android: 点菜单 → 添加到主屏幕"
echo ""
echo "  按 Ctrl+C 停止服务"
echo "=========================================="

python3 run_https.py
