#!/bin/bash
# AI热搜雷达 - 公网访问启动脚本
# 对方可以通过链接直接访问

echo "=========================================="
echo "  AI 热搜雷达 - 公网模式"
echo "=========================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

# 安装依赖
pip3 install -q fastapi uvicorn httpx beautifulsoup4 apscheduler 2>/dev/null

# 生成SSL证书
if [ ! -f "certs/cert.pem" ]; then
    mkdir -p certs
    openssl req -x509 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost" 2>/dev/null
fi

# 启动HTTPS服务（后台）
echo "启动服务..."
python3 run_https.py &
SERVER_PID=$!
sleep 3

# 检查cloudflared
CLOUDFLARED="/tmp/cloudflared"
if [ ! -f "$CLOUDFLARED" ]; then
    echo "下载cloudflared..."
    curl -sL "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64.tgz" -o /tmp/cloudflared.tgz
    tar -xzf /tmp/cloudflared.tgz -C /tmp/ 2>/dev/null
    chmod +x "$CLOUDFLARED" 2>/dev/null
fi

if [ -f "$CLOUDFLARED" ]; then
    echo ""
    echo "=========================================="
    echo "  启动成功！正在生成公网链接..."
    echo "=========================================="
    echo ""
    echo "  等待隧道建立（约10秒）..."
    echo ""

    # 启动隧道
    "$CLOUDFLARED" tunnel --url https://127.0.0.1:8443 2>&1 | grep -m1 "https://.*trycloudflare.com"

    echo ""
    echo "=========================================="
    echo "  把上面的链接发给对方即可！"
    echo "=========================================="
    echo ""
    echo "  对方操作："
    echo "  1. 打开链接"
    echo "  2. 忽略证书警告"
    echo "  3. iOS: 分享 → 添加到主屏幕"
    echo "  4. Android: 菜单 → 添加到主屏幕"
    echo ""
    echo "  按 Ctrl+C 停止"
    echo "=========================================="

    # 等待Ctrl+C
    trap "kill $SERVER_PID 2>/dev/null; exit" INT TERM
    wait
else
    echo "cloudflared 下载失败"
    echo "请手动安装: brew install cloudflared"
    kill $SERVER_PID 2>/dev/null
fi
