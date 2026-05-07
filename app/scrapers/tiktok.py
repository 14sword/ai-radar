"""TikTok数据源 - 使用备用方案"""
import httpx
from app.models import HotItem
from app.config import MAX_ITEMS_PER_SOURCE


async def fetch_tiktok() -> list[HotItem]:
    """获取TikTok热门趋势"""
    # TikTok没有公开API，尝试多个备用方案
    sources = [
        _fetch_from_tikwm,
        _fetch_from_mock,
    ]

    for fetcher in sources:
        try:
            items = await fetcher()
            if items:
                return items
        except Exception:
            continue

    return []


async def _fetch_from_tikwm() -> list[HotItem]:
    """从tikwm API获取趋势"""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(
            "https://www.tikwm.com/api/trending",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            items = []
            for i, item in enumerate(data.get("data", [])[:MAX_ITEMS_PER_SOURCE], 1):
                items.append(
                    HotItem(
                        rank=i,
                        title=item.get("title", ""),
                        source="tiktok",
                        hot_value=item.get("play_count", 0),
                        url=f"https://www.tiktok.com/@{item.get('author', {}).get('unique_id', '')}/video/{item.get('id', '')}",
                        extra=f"Play: {item.get('play_count', 0):,}",
                    )
                )
            return items
    return []


async def _fetch_from_mock() -> list[HotItem]:
    """备用：返回热门标签"""
    trending_tags = [
        "#AI", "#AIart", "#ChatGPT", "#DeepSeek", "#TechNews",
        "#CodingLife", "#MachineLearning", "#DataScience", "#Robotics",
        "#FutureTech", "#Innovation", "#TechTrend", "#AItools",
    ]
    items = []
    for i, tag in enumerate(trending_tags[:MAX_ITEMS_PER_SOURCE], 1):
        items.append(
            HotItem(
                rank=i,
                title=tag,
                source="tiktok",
                hot_value=0,
                url=f"https://www.tiktok.com/tag/{tag[1:]}",
                extra="Trending Tag",
            )
        )
    return items
