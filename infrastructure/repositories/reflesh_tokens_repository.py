from infrastructure.database.connection import get_connection, release_connection


class RefreshTokensRepository:

    async def save(self, user_id: int, token: str, expires_at=None) -> None:
        """
        Salva um refresh token para o usuário.
        """
        from datetime import datetime, timedelta

        if expires_at is None:
            expires_at = datetime.utcnow() + timedelta(days=1)

        conn = await get_connection()
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO refresh_tokens (user_id, token, expires_at)
                    VALUES (%s, %s, %s)
                    """,
                    (user_id, token, expires_at)
                )
                await conn.commit()
        finally:
            release_connection(conn)

    async def find_valid(self, token: str) -> dict | None:
        """
        Busca um refresh token válido (não revogado).
        """
        conn = await get_connection()
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT * FROM refresh_tokens WHERE token = %s AND is_revoked = 0",
                    (token,)
                )
                result = await cursor.fetchone()
                return result if result else None
        finally:
            release_connection(conn)

    async def revoke(self, token: str) -> None:
        """
        Revoga um refresh token específico.
        """
        conn = await get_connection()
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE refresh_tokens SET is_revoked = 1 WHERE token = %s",
                    (token,)
                )
                await conn.commit()
        finally:
            release_connection(conn)

    async def revoke_all_by_user_id(self, user_id: int) -> None:
        """
        Revoga todos os refresh tokens de um usuário.
        """
        conn = await get_connection()
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE refresh_tokens SET is_revoked = 1 WHERE user_id = %s",
                    (user_id,)
                )
                await conn.commit()
        finally:
            release_connection(conn)
