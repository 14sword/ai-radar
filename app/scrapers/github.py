import httpx
import logging
from datetime import datetime, timedelta
from app.models import HotItem
from app.config import MAX_ITEMS_PER_SOURCE

log = logging.getLogger(__name__)

GITHUB_SEARCH_API = "https://api.github.com/search/repositories"
GITHUB_HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Mozilla/5.0",
}


def _format_date(iso_str):
    """将ISO日期转换为相对时间"""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
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


async def fetch_github() -> list[HotItem]:
    """获取GitHub AI/ML热门仓库"""
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            date_30_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            resp = await client.get(
                GITHUB_SEARCH_API,
                params={
                    "q": f"topic:machine-learning created:>{date_30_days_ago}",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 20,
                },
                headers=GITHUB_HEADERS,
                timeout=8.0,
            )
        data = resp.json()
        items = []
        repos = data.get("items", [])

        for i, repo in enumerate(repos[:MAX_ITEMS_PER_SOURCE], 1):
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            lang = repo.get("language", "N/A") or "N/A"
            desc = (repo.get("description") or "")[:80]
            created = _format_date(repo.get("created_at"))
            updated = _format_date(repo.get("pushed_at") or repo.get("updated_at"))
            license_name = ""
            if repo.get("license") and repo["license"].get("spdx_id"):
                license_name = repo["license"]["spdx_id"]

            extra_parts = [f"⭐{stars:,}", f"🍴{forks}"]
            if license_name:
                extra_parts.append(license_name)
            extra_parts.append(updated)

            items.append(
                HotItem(
                    rank=i,
                    title=repo.get("full_name", ""),
                    source="github",
                    hot_value=stars,
                    url=repo.get("html_url", ""),
                    extra=" | ".join(extra_parts),
                    is_ai_related=True,
                    author=repo.get("owner", {}).get("login", ""),
                    views=stars,
                    likes=forks,
                    publish_time=created,
                    label=lang,
                )
            )
        return items
    except Exception as e:
        log.warning(f"GitHub fetch failed: {e}")
        return []
