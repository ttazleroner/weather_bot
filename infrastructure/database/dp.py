from psycopg_pool import AsyncConnectionPool
import logging
logger = logging.getLogger(__name__)

async def create_pool(dsn: str) -> AsyncConnectionPool:
    pool = AsyncConnectionPool(
        conninfo=dsn,
        open=False,
        min_size=1,
        max_size=10,
        timeout=10.0
    )

    try:
        print("⏳ Пытаюсь открыть пул соединений...")
        await pool.open()
        
        # проверка работает ли?)))
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT version();")
                version = await cur.fetchone()
                print(f"✅ УСПЕХ! База ответила: {version[0]}")
        
        return pool

    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА при подключении к БД: {e}")
        # если пул успел открыться, но проверка не прошла — закрываем
        await pool.close()
        # прокидываем ошибку дальше, чтобы бот упал и мы видели лог
        raise e
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # pool = AsyncConnectionPool(conninfo=dsn, open=False)
    # await pool.open()
    # print('Пул соединений с БД готов!')
    # return pool