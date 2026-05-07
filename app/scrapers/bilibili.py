import httpx
from app.models import HotItem, Creator
from app.config import BILIBILI_HEADERS, MAX_ITEMS_PER_SOURCE

BILIBILI_TRENDING_API = "https://api.bilibili.com/x/web-interface/wbi/search/square"
BILIBILI_SEARCH_API = "https://api.bilibili.com/x/web-interface/wbi/search/type"


async def fetch_bilibili() -> list[HotItem]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            BILIBILI_TRENDING_API,
            params={"limit": MAX_ITEMS_PER_SOURCE},
            headers=BILIBILI_HEADERS,
            timeout=10.0,
        )
        data = resp.json()
        items = []
        trending = data.get("data", {}).get("trending", {})
        word_list = trending.get("list", [])
        for i, item in enumerate(word_list[:MAX_ITEMS_PER_SOURCE], 1):
            keyword = item.get("keyword", "")
            heat_score = item.get("heat_score", 0)
            hot_id = item.get("hot_id", 0)
            items.append(
                HotItem(
                    rank=i,
                    title=keyword,
                    source="bilibili",
                    hot_value=hot_id,
                    url=f"https://search.bilibili.com/all?keyword={keyword}",
                    extra=f"热度 {heat_score:,}" if heat_score else f"热搜 #{i}",
                    views=heat_score,
                )
            )
        return items


async def fetch_bilibili_creators(keyword: str, limit: int = 10) -> list[Creator]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            BILIBILI_SEARCH_API,
            params={
                "search_type": "video",
                "keyword": keyword,
                "order": "click",
                "page": 1,
            },
            headers=BILIBILI_HEADERS,
            timeout=10.0,
        )
        data = resp.json()
        creators = []
        results = data.get("data", {}).get("result", [])
        seen_up = set()
        for item in results:
            up_name = item.get("author", "")
            if up_name in seen_up:
                continue
            seen_up.add(up_name)
            up_mid = item.get("mid", "")
            pic = item.get("pic", "")
            if pic and not pic.startswith("http"):
                pic = f"https:{pic}"
            creators.append(
                Creator(
                    name=up_name,
                    avatar=pic,
                    video_title=item.get("title", "").replace('<em class="keyword">', "").replace("</em>", ""),
                    video_url=f"https://www.bilibili.com/video/{item.get('bvid', '')}",
                    view_count=item.get("play", 0),
                )
            )
            if len(creators) >= limit:
                break
        return creators
