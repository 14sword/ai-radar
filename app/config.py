APP_TITLE = "热搜聚合看板"
HOST = "127.0.0.1"
PORT = 3000
REFRESH_INTERVAL_MINUTES = 5
MAX_ITEMS_PER_SOURCE = 50

HEADERS_DEFAULT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

BILIBILI_API = "https://api.bilibili.com/x/web-interface/ranking/v2"
BILIBILI_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com",
}

WEIBO_MOBILE_API = "https://m.weibo.cn/api/container/getIndex"
WEIBO_CONTAINER_ID = "106003type=25&t=3&disable_hot=1&filter_type=realtimehot"
WEIBO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Referer": "https://m.weibo.cn/",
}

TOPHUB_DOUYIN_URL = "https://tophub.today/n/DpQvNABoNE"
