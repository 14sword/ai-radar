"""ArXiv AI论文数据源"""
import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from app.models import HotItem
from app.config import MAX_ITEMS_PER_SOURCE
from app.http_client import get

log = logging.getLogger(__name__)

ARXIV_API = "https://export.arxiv.org/api/query"
ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}


def _format_date(entry):
    """从ArXiv条目中提取发布日期并格式化"""
    published = entry.find("atom:published", ARXIV_NS)
    if published is None or not published.text:
        return ""
    try:
        dt = datetime.fromisoformat(published.text.replace("Z", "+00:00"))
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


async def fetch_arxiv() -> list[HotItem]:
    """获取ArXiv最新AI/ML论文"""
    try:
        resp = await get(
            ARXIV_API,
            params={
                "search_query": "cat:cs.AI",
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "max_results": 15,
            },
            timeout=8.0,
        )
        root = ET.fromstring(resp.text)
        items = []

        for i, entry in enumerate(root.findall("atom:entry", ARXIV_NS)[:MAX_ITEMS_PER_SOURCE], 1):
            title_el = entry.find("atom:title", ARXIV_NS)
            link_el = entry.find("atom:id", ARXIV_NS)
            summary_el = entry.find("atom:summary", ARXIV_NS)

            # 提取作者
            authors = []
            for author_el in entry.findall("atom:author", ARXIV_NS):
                name_el = author_el.find("atom:name", ARXIV_NS)
                if name_el is not None and name_el.text:
                    authors.append(name_el.text.strip())

            title = (title_el.text or "").strip().replace("\n", " ") if title_el is not None else "Untitled"
            url = (link_el.text or "").strip() if link_el is not None else ""
            summary = (summary_el.text or "").strip()[:100] if summary_el is not None else ""

            pub_time = _format_date(entry)
            author_str = ", ".join(authors[:3])
            if len(authors) > 3:
                author_str += f" et al. ({len(authors)} authors)"

            extra_parts = ["ArXiv"]
            if author_str:
                extra_parts.append(author_str)
            if pub_time:
                extra_parts.append(pub_time)

            items.append(
                HotItem(
                    rank=i,
                    title=title,
                    source="arxiv",
                    hot_value=0,
                    url=url,
                    extra=" | ".join(extra_parts),
                    is_ai_related=True,
                    author=author_str,
                    publish_time=pub_time,
                )
            )
        return items
    except Exception as e:
        log.warning(f"ArXiv fetch failed: {e}")
        return []
