#!/bin/bash
# AI热搜雷达 - 启动脚本（macOS/Linux）

echo "=========================================="
echo "  AI 热搜雷达 - 启动中..."
echo "=========================================="

if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装"
    exit 1
fi

echo "检查依赖..."
pip3 install -q -r requirements.txt 2>/dev/null

LOCAL_IP=$(ifconfig 2>/dev/null | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

echo ""
echo "=========================================="
echo "  启动成功！"
echo "=========================================="
echo ""
echo "  电脑访问: http://127.0.0.1:8080"
[ -n "$LOCAL_IP" ] && echo "  手机访问: http://${LOCAL_IP}:8080"
echo ""
echo "  按 Ctrl+C 停止服务"
echo "=========================================="

python3 run.py
