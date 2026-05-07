import httpx
from datetime import datetime
from app.models import HotItem
from app.config import MAX_ITEMS_PER_SOURCE

KR36_AI_API = "https://gateway.36kr.com/api/mis/nav/home/nav/rank/hot"
KR36_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://36kr.com/",
    "Content-Type": "application/json",
}


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
                return f"{minutes}分钟前"
            return f"{hours}小时前"
        elif diff.days == 1:
            return "昨天"
        elif diff.days < 7:
            return f"{diff.days}天前"
        else:
            return dt.strftime("%m-%d")
    except Exception:
        return ""


async def fetch_36kr() -> list[HotItem]:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.post(
            KR36_AI_API,
            headers=KR36_HEADERS,
            json={
                "partner_id": "wap",
                "param": {
                    "siteId": 1,
                    "platformId": 2,
                },
                "timestamp": 0,
            },
            timeout=10.0,
        )
        data = resp.json()
        items = []
        hot_list = data.get("data", {}).get("hotRankList", [])
        for i, item in enumerate(hot_list[:MAX_ITEMS_PER_SOURCE], 1):
            material = item.get("templateMaterial", {})
            title = material.get("widgetTitle", "")
            item_id = item.get("itemId", "")
            url = f"https://36kr.com/p/{item_id}" if item_id else ""
            pub_time = _format_timestamp(material.get("publishTime"))
            views = material.get("statRead", 0)
            likes = material.get("statPraise", 0) or material.get("statCollect", 0)
            author = material.get("authorName", "")

            items.append(
                HotItem(
                    rank=i,
                    title=title,
                    source="36kr",
                    hot_value=views,
                    url=url,
                    extra=f"{author} | 阅读 {views:,}",
                    publish_time=pub_time,
                    views=views,
                    likes=likes,
                    author=author,
                )
            )
        return items
