#!/bin/bash
# 构建安卓APK

echo "=========================================="
echo "  AI热搜雷达 - 构建APK"
echo "=========================================="

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "错误: 未找到Node.js"
    echo "请先安装: https://nodejs.org"
    exit 1
fi

# 检查Android Studio
if [ ! -d "$HOME/Library/Android/sdk" ] && [ ! -d "$HOME/Android/Sdk" ]; then
    echo "错误: 未找到Android SDK"
    echo "请先安装Android Studio: https://developer.android.com/studio"
    exit 1
fi

# 安装依赖
echo "安装依赖..."
npm install

# 初始化Capacitor
echo "初始化Capacitor..."
npx cap init com.airadar.app "AI热搜雷达" --web-dir static

# 添加Android平台
echo "添加Android平台..."
npx cap add android

# 同步文件
echo "同步文件..."
npx cap sync

# 打开Android Studio
echo "打开Android Studio..."
npx cap open android

echo ""
echo "=========================================="
echo "  Android Studio已打开"
echo "=========================================="
echo ""
echo "  在Android Studio中："
echo "  1. 点 Build → Build Bundle(s) / APK(s)"
echo "  2. 选 Build APK(s)"
echo "  3. 等待构建完成"
echo "  4. APK文件在 app/build/outputs/apk/"
echo ""
echo "=========================================="
