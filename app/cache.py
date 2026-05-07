"""数据缓存模块 - 避免重复请求，失败时使用上次数据"""
import time
import logging
from typing import Any, Optional

log = logging.getLogger(__name__)


class DataCache:
    """简单的内存缓存"""

    def __init__(self, ttl_seconds: int = 300):
        """
        Args:
            ttl_seconds: 缓存过期时间（秒），默认5分钟
        """
        self._cache: dict[str, dict] = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        """获取缓存数据，过期返回None"""
        if key in self._cache:
            entry = self._cache[key]
            if time.time() - entry["time"] < self._ttl:
                return entry["data"]
            else:
                # 过期但保留，作为fallback
                return entry["data"]
        return None

    def set(self, key: str, data: Any):
        """设置缓存"""
        self._cache[key] = {
            "data": data,
            "time": time.time(),
        }

    def is_fresh(self, key: str) -> bool:
        """检查缓存是否新鲜（未过期）"""
        if key in self._cache:
            return time.time() - self._cache[key]["time"] < self._ttl
        return False


# 全局缓存实例
cache = DataCache(ttl_seconds=300)
