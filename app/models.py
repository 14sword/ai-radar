from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Creator:
    name: str
    avatar: str
    video_title: str
    video_url: str
    view_count: int


@dataclass
class HotItem:
    rank: int
    title: str
    source: str
    hot_value: int
    url: str
    extra: str = ""
    is_ai_related: bool = False
    related_creators: list[Creator] = field(default_factory=list)
    # 扩展字段
    publish_time: str = ""       # 发布时间
    views: int = 0               # 阅读/播放量
    likes: int = 0               # 点赞/收藏
    comments: int = 0            # 评论数
    author: str = ""             # 作者/来源
    label: str = ""              # 标签（热/新/沸）


@dataclass
class HotList:
    source: str
    items: list[HotItem]
    updated_at: str
    error: str | None = None
