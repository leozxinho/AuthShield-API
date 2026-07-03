import aiomysql

from infrastructure.database.connection import get_connection, release_connection


class PasswordHistoryRepository:
    """
    Responsável por todas as operações
    relacionadas à tabela password_history.
    """

    async def save(self, user_id: int, password_hash: str) -> None:
        """
        Salva uma senha no histórico.
        """
        conn = await get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO password_history
                    (user_id, password_hash)
                    VALUES (%s, %s)
                    """,
                    (user_id, password_hash)
                )
                await conn.commit()
        finally:
            release_connection(conn)

    async def get_last_passwords(self, user_id: int, limit: int = 5) -> list[str]:
        """
        Retorna os últimos N hashes de senha do usuário.
        """
        conn = await get_connection()

        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT password_hash
                    FROM password_history
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (user_id, limit)
                )
                results = await cursor.fetchall()
                return [row["password_hash"] for row in results]
        finally:
            release_connection(conn)
