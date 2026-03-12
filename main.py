import asyncio
import sys
import logging
from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from aiogram.fsm.storage.redis import RedisStorage
from handlers.start import router as start_router
from middleware.databse import DataBaseMiddleware
from infrastructure.database.dp import create_pool
from handlers.weather_fsm import router as weather_router
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# фикс от калловой винды
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    
    config: Config = load_config()
    
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    if config.redis.password:
        redis_url = f"redis://:{config.redis.password}@{config.redis.host}:{config.redis.port}/{config.redis.db_number}"
    else:
        redis_url = f"redis://{config.redis.host}:{config.redis.port}/{config.redis.db_number}"
    
    storage = RedisStorage.from_url(redis_url)
    
    dp = Dispatcher(storage=storage)
    
    logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
)
    
    logging.info(
        "😶‍🌫️Запуск..."
    )
    
    dsn = f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.database}"
    
    pool = await create_pool(dsn)
    if not pool:
        logging.error(" Не удалось подключиться к базе.")
        return
    
    dp.update.middleware(DataBaseMiddleware(pool=pool))
    
    # logging.basicConfig(
    #     level = config.log.level,
    #     format=config.log.format
    # )
    
    
    
    dp.include_routers(
        start_router,
        weather_router
        # help_message.router
    )
    

    
    await bot.delete_webhook(drop_pending_updates=True)
    
    
    await dp.start_polling(bot)
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен администратором')