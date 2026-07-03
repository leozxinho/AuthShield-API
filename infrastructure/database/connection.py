import aiomysql
from infrastructure.config.settings import get_settings



pool = None


async def create_pool():
    global pool
    settings = get_settings()
    pool = await aiomysql.create_pool(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        db=settings.DB_NAME,
        minsize=1,
        maxsize=10,
        autocommit=True,
    )


async def close_pool():
    global pool
    if pool is not None:
        pool.close()
        await pool.wait_closed()


async def get_connection():
    global pool
    if pool is None:
        await create_pool()
    return await pool.acquire()


def release_connection(conn):
    global pool
    if pool is not None:
        pool.release(conn)
