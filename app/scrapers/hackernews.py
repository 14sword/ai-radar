import httpx
import logging
from datetime import datetime, timezone
from app.models import HotItem
from app.config import MAX_ITEMS_PER_SOURCE

log = logging.getLogger(__name__)

HN_ALGOLIA_API = "https://hn.algolia.com/api/v1/search"


def _format_hn_time(created_at_i):
    """将HN时间戳转换为相对时间"""
    if not created_at_i:
        return ""
    try:
        dt = datetime.fromtimestamp(created_at_i, tz=timezone.utc)
        now = datetime.now(timezone.utc)
        diff = now - dt
        if diff.days == 0:
            hours = diff.seconds // 3600
            return f"{hours}h ago" if hours > 0 else "just now"
        elif diff.days < 7:
            return f"{diff.days}d ago"
        elif diff.days < 30:
            return f"{diff.days // 7}w ago"
        else:
            return dt.strftime("%Y-%m-%d")
    except Exception:
        return ""


async def fetch_hackernews() -> list[HotItem]:
    """获取HackerNews AI相关话题"""
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(
                HN_ALGOLIA_API,
                params={
                    "query": "AI OR LLM OR OpenAI OR model OR ML",
                    "tags": "story",
                    "hitsPerPage": 20,
                },
                timeout=8.0,
            )
        data = resp.json()
        items = []
        hits = data.get("hits", [])

        for i, hit in enumerate(hits[:MAX_ITEMS_PER_SOURCE], 1):
            points = hit.get("points", 0)
            comments = hit.get("num_comments", 0)
            author = hit.get("author", "")
            hn_url = f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            created = _format_hn_time(hit.get("created_at_i"))

            extra_parts = [f"▲{points}", f"💬{comments}"]
            if created:
                extra_parts.append(created)

            items.append(
                HotItem(
                    rank=i,
                    title=hit.get("title", ""),
                    source="hackernews",
                    hot_value=points,
                    url=hit.get("url") or hn_url,
                    extra=" | ".join(extra_parts),
                    is_ai_related=True,
                    views=points,
                    comments=comments,
                    author=author,
                    publish_time=created,
                )
            )
        return items
    except Exception as e:
        log.warning(f"HackerNews fetch failed: {e}")
        return []
