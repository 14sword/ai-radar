# AI 热搜雷达

实时追踪 AI 领域热点，聚合 B站、微博、抖音、GitHub、HackerNews、量子位、ArXiv、36Kr 等 10 个平台。

## 快速开始

### 方法一：一键启动（推荐）

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```
双击 start.bat
```

### 方法二：手动启动

```bash
pip install fastapi uvicorn httpx beautifulsoup4 apscheduler
python run_https.py
```

## 手机安装（PWA）

### 步骤

1. 确保手机和电脑连接同一 WiFi
2. 手机浏览器打开 `https://你的电脑IP:8443`
3. 忽略证书警告（自签名证书，点击"高级" → "继续访问"）
4. 安装到主屏幕：
   - **iOS**: 点击底部分享按钮 → "添加到主屏幕"
   - **Android**: 点击右上角菜单 → "添加到主屏幕"或"安装应用"

### 安装后

- 像原生 APP 一样全屏运行
- 独立图标，从主屏幕直接打开
- 60 秒自动刷新数据

## 分享给别人

### 方式一：直接分享文件夹

将整个项目文件夹打包发送，对方需要：
1. 安装 Python 3.10+
2. 运行 `start.sh` 或 `start.bat`

### 方式二：内网穿透（远程访问）

安装 [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/):

```bash
# macOS
brew install cloudflared

# 启动隧道
cloudflared tunnel --url https://127.0.0.1:8443
```

会生成一个公网 URL，分享给别人即可访问。

## 数据源

| 平台 | 说明 | 数量 |
|------|------|------|
| B站 | 热搜榜 | 50 |
| 微博 | 热搜榜 | 50 |
| 抖音 | 热搜榜 | 50 |
| TikTok | 热门趋势 | 10 |
| GitHub | AI/ML 热门仓库 | 20 |
| HackerNews | AI 话题 | 20 |
| 量子位 | AI 新闻 | 10 |
| ArXiv | AI 论文 | 15 |
| 36Kr | 科技快讯 | 50 |
| AI专题 | 多平台聚合 | 20+ |

## 功能特性

- 10 个数据源并行抓取
- AI 内容自动识别（88+ 关键词）
- 搜索过滤
- 时间筛选（今日/本周/本月）
- B站热搜展开查看相关博主
- 暗色赛博朋克主题
- 手机端适配

## 技术栈

- Python 3.10+
- FastAPI + Uvicorn
- httpx（异步HTTP）
- BeautifulSoup4（HTML解析）
- APScheduler（定时任务）
- 原生 HTML/CSS/JS（前端）

## 许可

MIT License
