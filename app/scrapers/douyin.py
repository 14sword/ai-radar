import httpx
from app.models import HotItem
from app.config import MAX_ITEMS_PER_SOURCE

DOUYIN_BILLBOARD_API = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
DOUYIN_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}


async def fetch_douyin() -> list[HotItem]:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(
            DOUYIN_BILLBOARD_API,
            headers=DOUYIN_HEADERS,
            timeout=10.0,
        )
        data = resp.json()
        items = []
        word_list = data.get("word_list", [])
        for i, item in enumerate(word_list[:MAX_ITEMS_PER_SOURCE], 1):
            keyword = item.get("word", "")
            hot_val = item.get("hot_value", 0)
            label = item.get("label", "") or ""
            url = f"https://www.douyin.com/search/{keyword}" if keyword else ""
            items.append(
                HotItem(
                    rank=i,
                    title=keyword,
                    source="douyin",
                    hot_value=hot_val,
                    url=url,
                    extra=f"热度 {hot_val:,}",
                    label=label,
                )
            )
        return items
