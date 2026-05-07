# AI 热搜雷达

> 实时追踪 AI 领域热点，聚合 10 个平台数据，科幻风格界面

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 项目简介

AI 热搜雷达是一个实时追踪 AI 领域热点的工具，聚合了 B站、微博、抖音、GitHub、HackerNews 等 10 个平台的数据，帮助用户快速了解 AI 领域的最新动态。

### 核心特性

- **10 个数据源** - 并行抓取，实时更新
- **AI 智能识别** - 88+ 关键词自动识别 AI 相关内容
- **科幻风格 UI** - 赛博朋克界面，动态效果
- **推送通知** - 新 AI 内容实时推送
- **移动端适配** - 手机端完美体验
- **PWA 支持** - 可添加到主屏幕，像 APP 一样使用

---

## 功能展示

### 主界面

```
┌─────────────────────────────────────────────────────────────┐
│  ◈ RADAR                    🔍 搜索...    247 TOTAL  64 AI  │
│    AI TREND MONITOR                                           │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                   │
│ ◈ 全部监控 │  HOT SEARCH                                      │
│ ⚡ AI专题  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│          │  │ 微博热搜      │ │ B站热搜      │ │ 抖音热搜    ││
│ ● 微博   │  │ 1. xxxxxx    │ │ 1. xxxxxx   │ │ 1. xxxxxx   ││
│ ● B站    │  │ 2. xxxxxx    │ │ 2. xxxxxx   │ │ 2. xxxxxx   ││
│ ● 抖音   │  │ 3. xxxxxx    │ │ 3. xxxxxx   │ │ 3. xxxxxx   ││
│ ● TikTok │  └─────────────┘ └─────────────┘ └─────────────┘│
│          │                                                   │
│ AI 专源   │  AI SOURCES                                      │
│ ● GitHub │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│ ● HN     │  │ GitHub AI    │ │ HackerNews  │ │ 量子位      ││
│ ● 量子位  │  │ 1. xxxxxx   │ │ 1. xxxxxx   │ │ 1. xxxxxx   ││
│ ● ArXiv  │  │ 2. xxxxxx   │ │ 2. xxxxxx   │ │ 2. xxxxxx   ││
│ ● 36Kr   │  └─────────────┘ └─────────────┘ └─────────────┘│
│          │                                                   │
│ ⏱ 24H历史 │                                                   │
└──────────┴──────────────────────────────────────────────────┘
```

### AI 专题视图

```
┌─────────────────────────────────────────────────────────────┐
│  ⚡ AI TRENDING                                             │
│  AGGREGATED · ALL · 24 ITEMS                                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. DeepSeek发布新模型，性能超越GPT-5      2h ago   │   │
│  │ 2. GitHub上最火的AI项目，Star破10万       5h ago   │   │
│  │ 3. 最新AI论文：多模态学习新突破           8h ago   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 移动端适配

```
┌───────────────────┐
│ ☰ AI 热搜雷达     │
├───────────────────┤
│ [全部] [AI] [微博] │
├───────────────────┤
│                   │
│ 微博热搜           │
│ 1. xxxxxx         │
│ 2. xxxxxx         │
│ 3. xxxxxx         │
│                   │
│ B站热搜           │
│ 1. xxxxxx         │
│ 2. xxxxxx         │
│                   │
└───────────────────┘
```

---

## 数据源

| 平台 | 类型 | 数量 | 说明 |
|------|------|------|------|
| B站 | 热搜榜 | 50 | 实时热搜关键词 |
| 微博 | 热搜榜 | 50 | 实时热搜关键词 |
| 抖音 | 热搜榜 | 50 | 实时热搜关键词 |
| TikTok | 热门趋势 | 13 | 热门标签和视频 |
| GitHub | AI仓库 | 20 | AI/ML 热门开源项目 |
| HackerNews | AI话题 | 20 | AI 相关技术讨论 |
| 量子位 | AI新闻 | 10 | AI 领域最新资讯 |
| ArXiv | AI论文 | 15 | 最新 AI/ML 学术论文 |
| 36Kr | 科技快讯 | 50 | 科技行业动态 |
| AI专题 | 聚合 | 24 | 多平台 AI 内容聚合 |

---

## 技术栈

### 后端

| 技术 | 用途 |
|------|------|
| Python 3.10+ | 主语言 |
| FastAPI | Web 框架 |
| Uvicorn | ASGI 服务器 |
| httpx | 异步 HTTP 客户端 |
| BeautifulSoup4 | HTML 解析 |
| APScheduler | 定时任务 |

### 前端

| 技术 | 用途 |
|------|------|
| HTML5 | 页面结构 |
| CSS3 | 样式和动画 |
| JavaScript | 交互逻辑 |
| PWA | 离线支持 |

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/14sword/ai-radar.git
cd ai-radar
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
python run.py
```

### 4. 访问

打开浏览器访问 http://127.0.0.1:8080

---

## 项目结构

```
ai-radar/
├── app/                    # 后端代码
│   ├── scrapers/           # 各平台爬虫
│   │   ├── bilibili.py     # B站
│   │   ├── weibo.py        # 微博
│   │   ├── douyin.py       # 抖音
│   │   ├── github.py       # GitHub
│   │   ├── hackernews.py   # HackerNews
│   │   ├── qbitai.py       # 量子位
│   │   ├── arxiv.py        # ArXiv
│   │   ├── kr36.py         # 36Kr
│   │   ├── tiktok.py       # TikTok
│   │   └── ai_hub.py       # AI专题聚合
│   ├── filters/            # 内容过滤
│   ├── main.py             # API路由
│   ├── scheduler.py        # 定时任务
│   ├── cache.py            # 数据缓存
│   └── models.py           # 数据模型
├── static/                 # 前端文件
│   ├── index.html          # 主页面
│   ├── style.css           # 样式
│   └── app.js              # 交互逻辑
├── requirements.txt        # 依赖列表
├── run.py                  # 启动脚本
└── README.md               # 项目说明
```

---

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/hot/all` | GET | 获取所有平台数据 |
| `/api/hot/{source}` | GET | 获取单平台数据 |
| `/api/sources` | GET | 获取数据源状态 |
| `/api/export/csv` | GET | 导出 CSV 文件 |
| `/api/export/json` | GET | 导出 JSON 文件 |

---

## 部署

### 本地部署

```bash
python run.py
```

### Railway 部署

1. Fork 本项目到你的 GitHub
2. 登录 [Railway](https://railway.app)
3. 选择 Deploy from GitHub repo
4. 选择本项目
5. 等待部署完成

### Docker 部署

```bash
docker build -t ai-radar .
docker run -p 8080:8080 ai-radar
```

---

## 功能特性

### 核心功能

- [x] 10 个数据源并行抓取
- [x] 60 秒自动刷新
- [x] AI 内容智能识别（88+ 关键词）
- [x] 搜索过滤功能
- [x] 数据导出（CSV/JSON）
- [x] 24 小时 AI 历史记录
- [x] 推送通知

### 界面特性

- [x] 赛博朋克科幻风格
- [x] 动态网格背景
- [x] 霓虹灯发光效果
- [x] 卡片入场动画
- [x] 响应式布局
- [x] 移动端手势支持

### 移动端特性

- [x] PWA 支持
- [x] 添加到主屏幕
- [x] 下拉刷新
- [x] 左右滑动切换平台

---

## AI 关键词列表

本项目使用 88+ 个关键词识别 AI 相关内容：

### 核心概念
AI、人工智能、机器学习、深度学习、大模型、大语言模型、LLM、AIGC、生成式AI、AGI

### 主流产品
ChatGPT、GPT-4、GPT-5、Claude、Gemini、Llama、Mistral、Qwen、通义千问、Grok

### 国内厂商
文心一言、豆包、Kimi、智谱、DeepSeek、DeepSeek-R1、百川、月之暗面、讯飞星火

### 技术概念
Transformer、神经网络、扩散模型、Stable Diffusion、Midjourney、Sora、LoRA

### 硬件芯片
英伟达、NVIDIA、GPU、算力、AI芯片、H100

### 应用领域
自动驾驶、智能驾驶、具身智能、多模态、机器人

---

## 更新日志

### v2.0 (2026-05-07)
- 新增赛博朋克科幻 UI
- 新增数据缓存机制
- 新增数据导出功能
- 新增 24H AI 历史记录
- 新增移动端手势支持
- 优化性能和加载速度

### v1.0 (2026-05-06)
- 初始版本发布
- 支持 10 个数据源
- 基础 UI 界面
- 自动刷新功能

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 许可证

MIT License

---

## 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Web 框架
- [httpx](https://www.python-httpx.org/) - 异步 HTTP 客户端
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析
