"""调度器模块 - 并行获取数据源，支持缓存"""
import asyncio
import logging
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scrapers import bilibili, weibo, douyin, kr36, ai_hub, tiktok, github, hackernews, qbitai, arxiv
from app.filters.ai_filter import is_ai_related
from app.cache import cache

log = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

# 24小时AI历史缓存
_ai_history: dict[str, dict] = {}
_history_lock = asyncio.Lock()

# 所有数据源
ALL_SCRAPERS = {
    "bilibili": bilibili.fetch_bilibili,
    "weibo": weibo.fetch_weibo,
    "douyin": douyin.fetch_douyin,
    "tiktok": tiktok.fetch_tiktok,
    "36kr": kr36.fetch_36kr,
    "github": github.fetch_github,
    "hackernews": hackernews.fetch_hackernews,
    "qbitai": qbitai.fetch_qbitai,
    "arxiv": arxiv.fetch_arxiv,
    "ai": ai_hub.fetch_ai_hub,
}

# AI专源（所有内容都是AI相关的）
AI_NATIVE_SOURCES = {"github", "hackernews", "qbitai", "arxiv", "ai"}

# 热搜平台（需要24小时历史）
HISTORY_PLATFORMS = {"bilibili", "weibo", "douyin"}


async def _fetch_one_source(source_name: str, fetcher, store):
    """获取单个数据源并更新store，支持缓存回退"""
    cache_key = f"source:{source_name}"

    try:
        items = await fetcher()

        if items:
            # 成功获取数据，更新缓存
            cache.set(cache_key, items)

            # 标记AI相关内容
            if source_name in AI_NATIVE_SOURCES:
                for item in items:
                    item.is_ai_related = True
            else:
                for item in items:
                    item.is_ai_related = is_ai_related(item.title)

            # 24小时历史缓存
            if source_name in HISTORY_PLATFORMS:
                await _merge_ai_history(source_name, items)

            await store.update(source_name, items)
            log.info(f"[OK] {source_name}: {len(items)} items")
        else:
            # 获取失败，尝试使用缓存
            cached = cache.get(cache_key)
            if cached:
                await store.update(source_name, cached)
                log.info(f"[CACHE] {source_name}: using cached {len(cached)} items")
            else:
                await store.update(source_name, [], error="No data")
                log.warning(f"[EMPTY] {source_name}: no data and no cache")

    except Exception as e:
        # 异常时使用缓存
        cached = cache.get(cache_key)
        if cached:
            await store.update(source_name, cached)
            log.info(f"[CACHE] {source_name}: using cached {len(cached)} items (error: {e})")
        else:
            await store.update(source_name, [], error=str(e))
            log.warning(f"[FAIL] {source_name}: {e}")


async def fetch_all_sources(store):
    """并行获取所有数据源"""
    tasks = [
        _fetch_one_source(name, fetcher, store)
        for name, fetcher in ALL_SCRAPERS.items()
    ]
    await asyncio.gather(*tasks)


async def _merge_ai_history(platform: str, fresh_items):
    """合并AI内容到24小时历史"""
    now = datetime.now(timezone.utc)
    async with _history_lock:
        if platform not in _ai_history:
            _ai_history[platform] = {}

        hist = _ai_history[platform]

        # 过期超过24小时的条目
        expired = [k for k, v in hist.items() if (now - v["first_seen"]).total_seconds() > 86400]
        for k in expired:
            del hist[k]

        # 合并新的AI内容
        for item in fresh_items:
            if not item.is_ai_related:
                continue
            key = item.title[:30]
            if key in hist:
                existing = hist[key]
                existing["heat_score"] = item.hot_value
                existing["rank"] = item.rank
                existing["author"] = item.author or existing.get("author", "")
            else:
                hist[key] = {
                    "title": item.title,
                    "url": item.url,
                    "rank": item.rank,
                    "platform": platform,
                    "heat_score": item.hot_value,
                    "heat_display": item.extra,
                    "is_ai_related": True,
                    "author": item.author,
                    "first_seen": now,
                }


def get_ai_history(platform: str) -> list:
    """获取平台的24小时AI历史"""
    hist = _ai_history.get(platform, {})
    items = list(hist.values())
    items.sort(key=lambda x: x.get("first_seen", datetime.min), reverse=True)
    return items


def setup_scheduler(store, interval_minutes=1):
    scheduler.add_job(
        fetch_all_sources,
        "interval",
        minutes=interval_minutes,
        args=[store],
        id="hot_list_fetcher",
        max_instances=1,
    )
    scheduler.start()
