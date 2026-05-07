"""共享HTTP客户端 - 统一的请求配置和连接池"""
import httpx
from typing import Optional

# 默认配置
DEFAULT_TIMEOUT = 10.0
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 全局客户端实例
_client: Optional[httpx.AsyncClient] = None


async def get_client() -> httpx.AsyncClient:
    """获取共享的HTTP客户端"""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=DEFAULT_TIMEOUT,
            follow_redirects=True,
            limits=httpx.Limits(
                max_connections=20,
                max_keepalive_connections=10,
            ),
        )
    return _client


async def close_client():
    """关闭HTTP客户端"""
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
        _client = None


async def get(url: str, headers: Optional[dict] = None, timeout: float = DEFAULT_TIMEOUT, **kwargs) -> httpx.Response:
    """GET请求，支持自定义headers和超时"""
    client = await get_client()
    merged_headers = {**DEFAULT_HEADERS, **(headers or {})}
    return await client.get(url, headers=merged_headers, timeout=timeout, **kwargs)


async def post(url: str, headers: Optional[dict] = None, json: Optional[dict] = None, timeout: float = DEFAULT_TIMEOUT, **kwargs) -> httpx.Response:
    """POST请求"""
    client = await get_client()
    merged_headers = {**DEFAULT_HEADERS, **(headers or {})}
    return await client.post(url, headers=merged_headers, json=json, timeout=timeout, **kwargs)
