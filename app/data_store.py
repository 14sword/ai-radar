import asyncio
from datetime import datetime
from app.models import HotItem, HotList


class DataStore:
    def __init__(self):
        self._data: dict[str, HotList] = {}
        self._lock = asyncio.Lock()

    async def update(self, source: str, items: list[HotItem], error: str | None = None):
        async with self._lock:
            self._data[source] = HotList(
                source=source,
                items=items,
                updated_at=datetime.now().isoformat(),
                error=error,
            )

    def get(self, source: str) -> HotList | None:
        return self._data.get(source)

    def get_all(self) -> dict[str, HotList]:
        return dict(self._data)
