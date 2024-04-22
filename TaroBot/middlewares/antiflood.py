from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import Message
from cachetools import TTLCache

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int=1):
        self.limit = TTLCache(maxsize=10000, ttl=time_limit)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.chat.id in self.limit:
            return event.answer('Не так быстро, помедленней)')
        else:
            self.limit[event.chat.id] = None
        return await handler(event, data)