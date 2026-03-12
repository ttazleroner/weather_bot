from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

class TestMiddleware(BaseMiddleware):
    async def __call__(
    self,
    handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
    event: TelegramObject,
    data: Dict[str, Any]
    ) -> Any:
        
        print("🔴 [1] Мидлварь: Апдейт зашел. Передаю дальше...")
        
        result = await handler(event,data)
        
        print("🟢 [3] Мидлварь: Хэндлер отработал. Апдейт возвращается.")
        
        return result
