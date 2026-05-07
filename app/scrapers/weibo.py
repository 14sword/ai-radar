import httpx
from app.models import HotItem
from app.config import MAX_ITEMS_PER_SOURCE

WEIBO_DESKTOP_API = "https://weibo.com/ajax/side/hotSearch"
WEIBO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://weibo.com/",
}


async def fetch_weibo() -> list[HotItem]:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(
            WEIBO_DESKTOP_API,
            headers=WEIBO_HEADERS,
            timeout=10.0,
        )
        data = resp.json()
        items = []
        realtime = data.get("data", {}).get("realtime", [])
        for i, item in enumerate(realtime[:MAX_ITEMS_PER_SOURCE], 1):
            keyword = item.get("note", item.get("word", ""))
            hot_val = item.get("num", 0)
            label = item.get("label_name", "")
            title = f"[{label}] {keyword}" if label else keyword
            items.append(
                HotItem(
                    rank=i,
                    title=title,
                    source="weibo",
                    hot_value=hot_val,
                    url=f"https://s.weibo.com/weibo?q={keyword}",
                    extra=f"热度 {hot_val:,}",
                    label=label,
                )
            )
        return items
