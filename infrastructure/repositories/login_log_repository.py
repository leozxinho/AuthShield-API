from infrastructure.database.connection import get_connection, release_connection


class LoginLogRepository:
    """
    Responsável por todas as operações
    relacionadas à tabela login_logs.
    """

    async def create_log(self, user_id: int, ip_address: str, user_agent: str, success: bool) -> None:
        """
        Salva um registro de tentativa de login.
        """
        conn = await get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO login_logs
                    (user_id, ip_address, user_agent, success)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user_id, ip_address, user_agent, success)
                )
                await conn.commit()
        finally:
            release_connection(conn)
            
            
    async def get_known_ips(self, user_id: int) -> list[str]:
        """
        Retorna uma lista de endereços IP conhecidos para o usuário.
        """
        conn = await get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT DISTINCT ip_address
                    FROM login_logs
                    WHERE user_id = %s AND success = TRUE
                    """,
                    (user_id,)
                )
                results = await cursor.fetchall()
                return [row[0] for row in results]
        finally:
            release_connection(conn)