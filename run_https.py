"""AI热搜雷达 - HTTPS启动脚本（支持PWA安装）"""
import ssl
import uvicorn
from app.main import create_app
from app.config import HOST

app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("  AI 热搜雷达 - HTTPS Mode")
    print("=" * 50)
    print()
    print("  本机访问: https://127.0.0.1:8443")
    print()
    print("  手机访问步骤:")
    print("  1. 确保手机和电脑在同一WiFi")
    print("  2. 手机浏览器打开: https://你的电脑IP:8443")
    print("  3. 忽略证书警告（自签名证书）")
    print("  4. iOS: 分享按钮 → 添加到主屏幕")
    print("  5. Android: 菜单 → 添加到主屏幕")
    print()
    print("  按 Ctrl+C 停止服务")
    print("=" * 50)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8443,
        ssl_keyfile="certs/key.pem",
        ssl_certfile="certs/cert.pem",
    )
