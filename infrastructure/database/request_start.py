from psycopg import AsyncConnection

async def add_user_to_db(conn: AsyncConnection, user_id: int, username: str):
    async with conn.cursor() as cur:
        await cur.execute(
            """
            INSERT INTO users (user_id, username, role, language, is_alive, banned)
            VALUES (%s, %s, 'user', 'ru', true, false)
            ON CONFLICT (user_id) DO NOTHING
            """,
            (user_id, username)
            
        )
        await conn.commit()

async def check_users(conn: AsyncConnection) -> int: # ДЛЯ ПОДСЧЕТА ЮЗЕРОВ В БД 
    async with conn.cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM users")
        result = await cur.fetchone()
        if not result:
            return 0
        return result[0]

async def check_activity(conn:AsyncConnection, user_id: str):
    async with conn.cursor() as cur:
        await cur.execute(
            """
            INSERT INTO activity (user_id, activity_date, actions)
            VALUES (%s, CURRENT_DATE, 1)
            ON CONFLICT (user_id, activity_date) 
            DO UPDATE SET actions = activity.actions + 1;
            """,
            (user_id,)
        )