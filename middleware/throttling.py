import time
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

# МИДЛВАРЬ ОТ СПАМА ( ДЕЛАЕТ ПАУЗУ В 1.5 СЕКУНД ) ANTI-SPAM
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 1.0):
        self.limit = limit
        self.users = {}
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        
        event: TelegramObject,
        
        data: Dict[str,Any]
        
        
        
    ) -> Any:
        
        user = data.get('event_from_user')
        
        if user:
            user_id = user.id
            current_time = time.time()
            last_time = self.users.get(user_id, 0)
            
            if current_time - last_time < self.limit:
                print(f'Юзер {user_id} спамит! Блокируем.')
                
                return
            
            self.users[user_id] = current_time
            
        return await handler(event,data)