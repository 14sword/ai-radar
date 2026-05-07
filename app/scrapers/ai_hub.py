import asyncio
import httpx
from datetime import datetime, timedelta
from app.models import HotItem
from app.config import MAX_ITEMS_PER_SOURCE


async def fetch_ai_hub() -> list[HotItem]:
    """聚合多个来源的AI相关内容，只保留近期内容"""
    items = []

    # 从36kr获取AI相关（主要来源，有时间信息）
    try:
        kr36_items = await _fetch_36kr_ai()
        items.extend(kr36_items)
    except Exception:
        pass

    # 从微博热搜筛选AI相关
    try:
        weibo_items = await _fetch_weibo_ai()
        items.extend(weibo_items)
    except Exception:
        pass

    # 去重并按时间排序（最新的在前）
    seen_titles = set()
    unique_items = []
    for item in items:
        # 简单去重
        title_key = item.title[:20]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_items.append(item)

    # 按热度排序
    unique_items.sort(key=lambda x: x.hot_value, reverse=True)

    return unique_items[:MAX_ITEMS_PER_SOURCE]


async def _fetch_36kr_ai() -> list[HotItem]:
    """从36kr获取AI相关文章（主要来源）"""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.post(
            "https://gateway.36kr.com/api/mis/nav/home/nav/rank/hot",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Referer": "https://36kr.com/",
                "Content-Type": "application/json",
            },
            json={"partner_id": "wap", "param": {"siteId": 1, "platformId": 2}, "timestamp": 0},
            timeout=10.0,
        )
        data = resp.json()
        items = []
        hot_list = data.get("data", {}).get("hotRankList", [])

        for item in hot_list:
            material = item.get("templateMaterial", {})
            title = material.get("widgetTitle", "")

            # 只保留AI相关内容
            if _is_ai_content(title):
                item_id = item.get("itemId", "")
                pub_ts = material.get("publishTime")
                pub_time = _format_timestamp(pub_ts) if pub_ts else ""
                views = material.get("statRead", 0)
                likes = material.get("statPraise", 0) or material.get("statCollect", 0)
                author = material.get("authorName", "")

                items.append(
                    HotItem(
                        rank=len(items) + 1,
                        title=title,
                        source="ai",
                        hot_value=views,
                        url=f"https://36kr.com/p/{item_id}" if item_id else "",
                        extra=f"36Kr | {author}",
                        publish_time=pub_time,
                        views=views,
                        likes=likes,
                        author=author,
                    )
                )
        return items[:20]


async def _fetch_weibo_ai() -> list[HotItem]:
    """从微博热搜筛选AI相关"""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(
            "https://weibo.com/ajax/side/hotSearch",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Referer": "https://weibo.com/",
            },
            timeout=10.0,
        )
        data = resp.json()
        items = []
        realtime = data.get("data", {}).get("realtime", [])

        for item in realtime:
            word = item.get("note", item.get("word", ""))
            if _is_ai_content(word):
                items.append(
                    HotItem(
                        rank=len(items) + 1,
                        title=word,
                        source="ai",
                        hot_value=item.get("num", 0),
                        url=f"https://s.weibo.com/weibo?q={word}",
                        extra=f"微博热搜 | 热度 {item.get('num', 0):,}",
                        label=item.get("label_name", ""),
                    )
                )
        return items[:10]


def _format_timestamp(ts):
    """将毫秒时间戳转换为可读时间"""
    if not ts:
        return ""
    try:
        dt = datetime.fromtimestamp(ts / 1000)
        now = datetime.now()
        diff = now - dt
        if diff.days == 0:
            hours = diff.seconds // 3600
            if hours == 0:
                minutes = diff.seconds // 60
                return f"{minutes}分钟前" if minutes > 0 else "刚刚"
            return f"{hours}小时前"
        elif diff.days == 1:
            return "昨天"
        elif diff.days < 7:
            return f"{diff.days}天前"
        elif diff.days < 30:
            weeks = diff.days // 7
            return f"{weeks}周前"
        elif diff.days < 365:
            months = diff.days // 30
            return f"{months}个月前"
        else:
            return dt.strftime("%Y-%m-%d")
    except Exception:
        return ""


def _is_ai_content(title: str) -> bool:
    """检测是否为AI相关内容"""
    ai_keywords = [
        "AI", "ai", "人工智能", "大模型", "DeepSeek", "deepseek",
        "ChatGPT", "chatgpt", "Claude", "claude", "Gemini", "gemini",
        "智能", "机器学习", "深度学习", "GPT", "AIGC", "算法",
        "英伟达", "NVIDIA", "GPU", "芯片", "算力", "机器人",
        "自动驾驶", "智能驾驶", "文心", "通义", "豆包", "Kimi",
        "MiniMax", "智谱", "百川", "月之暗面", "零一万物",
    ]
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in ai_keywords)
