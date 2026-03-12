from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from psycopg_pool import AsyncConnectionPool

class DataBaseMiddleware(BaseMiddleware):
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self.pool.connection() as conn:
            data['conn'] = conn
            return await handler(event, data)