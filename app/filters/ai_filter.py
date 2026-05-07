AI_KEYWORDS = [
    # ===== 核心AI概念 (12) =====
    "AI",
    "人工智能",
    "机器学习",
    "深度学习",
    "大模型",
    "大语言模型",
    "LLM",
    "AIGC",
    "生成式AI",
    "AGI",
    "生成式",
    "智算",

    # ===== 主流产品 (12) =====
    "ChatGPT",
    "GPT-4",
    "GPT-5",
    "GPT",
    "Claude",
    "Gemini",
    "Llama",
    "Mistral",
    "Qwen",
    "通义千问",
    "Grok",
    "Copilot",

    # ===== 国内厂商 (14) =====
    "文心一言",
    "文心",
    "豆包",
    "Kimi",
    "智谱",
    "DeepSeek",
    "DeepSeek-R1",
    "百川",
    "月之暗面",
    "零一万物",
    "讯飞星火",
    "讯飞",
    "商汤",
    "MiniMax",

    # ===== AI应用 (12) =====
    "AI绘画",
    "AI写作",
    "AI视频",
    "AI音乐",
    "AI换脸",
    "AI配音",
    "AI客服",
    "AI搜索",
    "AI编程",
    "智能体",
    "Agent",
    "RAG",

    # ===== 技术概念 (12) =====
    "Transformer",
    "神经网络",
    "扩散模型",
    "Stable Diffusion",
    "Midjourney",
    "Sora",
    "可灵",
    "LoRA",
    "向量数据库",
    "token",
    "大算力",
    "智算中心",

    # ===== 硬件芯片 (8) =====
    "英伟达",
    "NVIDIA",
    "GPU",
    "算力",
    "AI芯片",
    "H100",
    "B200",
    "昇腾",

    # ===== 应用领域 (8) =====
    "自动驾驶",
    "智能驾驶",
    "具身智能",
    "多模态",
    "机器人",
    "无人机",
    "智慧城市",
    "数字人",

    # ===== 行业动态 (10) =====
    "人工智能大会",
    "世界人工智能",
    "AI大会",
    "大模型备案",
    "AI监管",
    "AI安全",
    "AI伦理",
    "AI失业",
    "AI替代",
    "AI革命",
]

# 合并重复并去重
AI_KEYWORDS = list(dict.fromkeys(AI_KEYWORDS))


def is_ai_related(title: str) -> bool:
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in AI_KEYWORDS)
