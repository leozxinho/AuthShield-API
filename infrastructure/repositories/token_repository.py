from infrastructure.database.connection import get_connection, release_connection


async def add_to_blacklist(token: str, expired_at: str):
    """
    Adiciona um token à lista negra.
    """
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                INSERT INTO token_blacklist (token, expired_at)
                VALUES (%s, %s)
            """, (token, expired_at))
            await conn.commit()
    finally:
        release_connection(conn)


async def is_token_blacklisted(token: str) -> bool:
    """
    Verifica se um token está na lista negra.
    """
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                SELECT COUNT(*) FROM token_blacklist WHERE token = %s
            """, (token,))
            result = await cursor.fetchone()
            return result[0] > 0
    finally:
        release_connection(conn)
