#!/bin/bash
# AI 热搜雷达 // AI Radar Launcher
# ----------------------------------------------------
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT" || exit 1

echo "====== AI 热搜雷达 // AI Radar ======"

PORT=8080

# 1. 检查服务是否已在运行
nc -z localhost $PORT >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "[✓] 检测到 AI 雷达服务已在运行。"
else
    echo "[...] 正在拉起 FastAPI 后端服务..."
    
    # 优先检测是否通过 Homebrew 服务安装并配置
    if command -v brew &> /dev/null && brew services list 2>/dev/null | grep -q "ai-radar"; then
        echo "[...] 检测到已安装 Homebrew 服务，正在启动..."
        brew services start ai-radar
        sleep 2
    else
        # 否则使用本地虚拟环境启动
        echo "[!] 本地虚拟环境拉起中..."
        if [ ! -d ".venv" ]; then
            python3 -m venv .venv
        fi
        source .venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        python3 run.py > /dev/null 2>&1 &
        BACKEND_PID=$!
        sleep 2
    fi
    
    # 等待服务端口就绪
    for i in {1..5}; do
        nc -z localhost $PORT >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "[✓] 服务已就绪。"
            break
        fi
        sleep 1
    done
fi

# 2. 自动打开浏览器界面
echo "[...] 正在打开 AI 热搜雷达看板..."
if command -v open &> /dev/null; then
    open "http://localhost:$PORT"
else
    echo "请手动在浏览器中访问: http://localhost:$PORT"
fi

# 3. 退出清理 (如果是本地进程)
if [ ! -z "$BACKEND_PID" ]; then
    echo ""
    read -p "是否终止本地后台启动的服务进程？(Y/n): " stop_backend
    if [[ "$stop_backend" =~ ^[Yy]*$ ]] || [ -z "$stop_backend" ]; then
        kill $BACKEND_PID
        echo "[✓] 服务已安全关闭。"
    fi
fi
