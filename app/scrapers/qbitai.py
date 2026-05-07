import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from app.models import HotItem
from app.config import MAX_ITEMS_PER_SOURCE

QBITAI_RSS = "https://www.qbitai.com/feed"


def _format_pub_date(date_str):
    """将RSS日期转换为相对时间"""
    if not date_str:
        return ""
    try:
        # RSS日期格式: "Thu, 08 May 2025 10:30:00 +0800"
        dt = datetime.strptime(date_str.strip(), "%a, %d %b %Y %H:%M:%S %z")
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


async def fetch_qbitai() -> list[HotItem]:
    """获取量子位AI新闻RSS"""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(
            QBITAI_RSS,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15.0,
        )
        root = ET.fromstring(resp.text)
        items = []

        for i, item in enumerate(root.findall(".//item")[:MAX_ITEMS_PER_SOURCE], 1):
            title_el = item.find("title")
            link_el = item.find("link")
            desc_el = item.find("description")
            pub_date_el = item.find("pubDate")
            creator_el = item.find("{http://purl.org/dc/elements/1.1/}creator")

            title = (title_el.text or "").strip() if title_el is not None else ""
            url = (link_el.text or "").strip() if link_el is not None else ""
            desc = (desc_el.text or "").strip()[:80] if desc_el is not None else ""
            pub_date = (pub_date_el.text or "").strip() if pub_date_el is not None else ""
            author = (creator_el.text or "").strip() if creator_el is not None else ""

            pub_time = _format_pub_date(pub_date)

            if title:
                extra_parts = ["量子位"]
                if author:
                    extra_parts.append(author)
                if pub_time:
                    extra_parts.append(pub_time)

                items.append(
                    HotItem(
                        rank=i,
                        title=title,
                        source="qbitai",
                        hot_value=0,
                        url=url,
                        extra=" | ".join(extra_parts),
                        is_ai_related=True,
                        author=author,
                        publish_time=pub_time,
                    )
                )
        return items
