import csv
import io
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from app.data_store import DataStore
from app.scheduler import setup_scheduler, fetch_all_sources, get_ai_history
from app.config import APP_TITLE, REFRESH_INTERVAL_MINUTES
from app.scrapers.bilibili import fetch_bilibili_creators

store = DataStore()

PLATFORM_NAMES = {
    "bilibili": "B站",
    "weibo": "微博",
    "douyin": "抖音",
    "tiktok": "TikTok",
    "36kr": "36Kr",
    "github": "GitHub",
    "hackernews": "HackerNews",
    "qbitai": "量子位",
    "ai": "AI专题",
}


def serialize_item(item):
    return {
        "rank": item.rank,
        "title": item.title,
        "source": item.source,
        "hot_value": item.hot_value,
        "url": item.url,
        "extra": item.extra,
        "is_ai_related": item.is_ai_related,
        "publish_time": item.publish_time,
        "views": item.views,
        "likes": item.likes,
        "comments": item.comments,
        "author": item.author,
        "label": item.label,
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    await fetch_all_sources(store)
    setup_scheduler(store, interval_minutes=REFRESH_INTERVAL_MINUTES)
    yield


def create_app():
    app = FastAPI(title=APP_TITLE, lifespan=lifespan)

    @app.get("/api/hot/all")
    async def get_all_hot(ai_only: bool = False, limit: int = 50):
        result = {}
        for source_name, hot_list in store.get_all().items():
            items = hot_list.items
            if ai_only:
                # 热搜平台使用24小时历史
                if source_name in {"bilibili", "weibo", "douyin"}:
                    history = get_ai_history(source_name)
                    items = [
                        type("Item", (), {
                            "rank": h["rank"],
                            "title": h["title"],
                            "source": source_name,
                            "hot_value": h["heat_score"],
                            "url": h["url"],
                            "extra": h.get("heat_display", ""),
                            "is_ai_related": True,
                            "publish_time": "",
                            "views": h["heat_score"],
                            "likes": 0,
                            "comments": 0,
                            "author": h.get("author", ""),
                            "label": "",
                        })()
                        for h in history
                    ]
                else:
                    items = [i for i in items if i.is_ai_related]
            items = items[:limit]
            result[source_name] = {
                "source": hot_list.source,
                "updated_at": hot_list.updated_at,
                "error": hot_list.error,
                "items": [
                    {**serialize_item(i), "rank": idx + 1}
                    for idx, i in enumerate(items)
                ],
            }
        return {"code": 0, "data": result}

    @app.get("/api/hot/{source}")
    async def get_hot(source: str, ai_only: bool = False, limit: int = 50):
        hot_list = store.get(source)
        if not hot_list:
            return {"code": 1, "message": "数据未就绪"}
        items = hot_list.items
        if ai_only:
            items = [i for i in items if i.is_ai_related]
        items = items[:limit]
        return {
            "code": 0,
            "data": {
                "source": hot_list.source,
                "updated_at": hot_list.updated_at,
                "error": hot_list.error,
                "items": [
                    {**serialize_item(i), "rank": idx + 1}
                    for idx, i in enumerate(items)
                ],
            },
        }

    @app.get("/api/bilibili/creators")
    async def get_bilibili_creators(keyword: str, limit: int = 10):
        try:
            creators = await fetch_bilibili_creators(keyword, limit)
            return {
                "code": 0,
                "data": [
                    {
                        "name": c.name,
                        "avatar": c.avatar,
                        "video_title": c.video_title,
                        "video_url": c.video_url,
                        "view_count": c.view_count,
                    }
                    for c in creators
                ],
            }
        except Exception as e:
            return {"code": 1, "message": str(e)}

    @app.get("/api/sources")
    async def get_sources():
        sources = {}
        for name, hot_list in store.get_all().items():
            sources[name] = {
                "updated_at": hot_list.updated_at,
                "count": len(hot_list.items),
                "error": hot_list.error,
            }
        return {"code": 0, "data": sources}

    @app.get("/api/export/csv")
    async def export_csv(ai_only: bool = True):
        """导出AI相关趋势为CSV"""
        output = io.StringIO()
        output.write("﻿")  # UTF-8 BOM for Excel
        writer = csv.writer(output)
        writer.writerow(["平台", "排名", "标题", "热度值", "作者", "链接", "AI相关"])

        for source_name, hot_list in store.get_all().items():
            items = hot_list.items
            if ai_only:
                items = [i for i in items if i.is_ai_related]

            for i, item in enumerate(items[:50], 1):
                writer.writerow([
                    PLATFORM_NAMES.get(source_name, source_name),
                    i,
                    item.title,
                    item.hot_value,
                    item.author,
                    item.url,
                    "是" if item.is_ai_related else "否",
                ])

        output.seek(0)
        return Response(
            output.getvalue().encode("utf-8-sig"),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=ai-trends.csv"},
        )

    @app.get("/api/export/json")
    async def export_json(ai_only: bool = True):
        """导出AI相关趋势为JSON"""
        result = {}
        for source_name, hot_list in store.get_all().items():
            items = hot_list.items
            if ai_only:
                items = [i for i in items if i.is_ai_related]
            result[source_name] = [
                {
                    "rank": i + 1,
                    "title": item.title,
                    "hot_value": item.hot_value,
                    "author": item.author,
                    "url": item.url,
                    "publish_time": item.publish_time,
                }
                for i, item in enumerate(items[:50])
            ]
        return Response(
            json.dumps(result, ensure_ascii=False, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=ai-trends.json"},
        )

    @app.get("/")
    async def index():
        return FileResponse("static/index.html")

    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app
