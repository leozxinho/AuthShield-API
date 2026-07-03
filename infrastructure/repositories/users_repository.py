# Cursor que retorna dicionários ao invés de tuplas
import aiomysql


# Pool de conexões
from domain.entities.users import User
from infrastructure.database.connection import (
    get_connection,
    release_connection
)


class UserRepository:
    """
    Responsável por todas as operações
    relacionadas à tabela users.
    """

    async def find_by_email(
        self,
        email: str
    ) -> User | None:
        """
        Busca um usuário pelo email.
        """

        conn = await get_connection()

        try:

            async with conn.cursor(
                aiomysql.DictCursor
            ) as cursor:

                await cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        email,
                        password_hash,
                        is_verified,
                        is_active,
                        locked_until,
                        failed_login_attempts,
                        password_changed_at,
                        verification_token,
                        created_at
                    FROM users
                    WHERE email = %s
                    """,
                    (email,)
                )

                result = await cursor.fetchone()

                if not result:
                    return None

                return User(
                    id=result["id"],
                    name=result["name"],
                    email=result["email"],
                    password_hash=result["password_hash"],
                    is_verified=result["is_verified"],
                    is_active=result["is_active"],
                    locked_until=result["locked_until"],
                    failed_login_attempts=result["failed_login_attempts"],
                    password_changed_at=result["password_changed_at"],
                    verification_token=result["verification_token"],
                    created_at=result["created_at"]
                )

        finally:

            release_connection(conn)

    async def find_by_id(
        self,
        user_id: int
    ) -> User | None:
        """
        Busca usuário pelo ID.
        """

        conn = await get_connection()

        try:

            async with conn.cursor(
                aiomysql.DictCursor
            ) as cursor:

                await cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        email,
                        password_hash,
                        is_verified,
                        is_active,
                        locked_until,
                        failed_login_attempts,
                        password_changed_at,
                        verification_token,
                        created_at
                    FROM users
                    WHERE id = %s
                    """,
                    (user_id,)
                )

                result = await cursor.fetchone()

                if not result:
                    return None

                return User(
                    id=result["id"],
                    name=result["name"],
                    email=result["email"],
                    password_hash=result["password_hash"],
                    is_verified=result["is_verified"],
                    is_active=result["is_active"],
                    locked_until=result["locked_until"],
                    failed_login_attempts=result["failed_login_attempts"],
                    password_changed_at=result["password_changed_at"],
                    verification_token=result["verification_token"],
                    created_at=result["created_at"]
                )

        finally:

            release_connection(conn)

    async def create(
        self,
        name: str,
        email: str,
        password_hash: str
    ) -> int:
        """
        Cria um novo usuário.
        Retorna o ID gerado.
        """

        conn = await get_connection()

        try:

            async with conn.cursor() as cursor:

                await cursor.execute(
                    """
                    INSERT INTO users
                    (
                        name,
                        email,
                        password_hash
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        name,
                        email,
                        password_hash
                    )
                )

                # ID gerado pelo MySQL
                return cursor.lastrowid

        finally:

            release_connection(conn)
            
            
    async def increment_failed_login_attempts(self, user_id: int) -> None: # Responsável por incrementar o contador de tentativas de login falhas para um usuário.
        """
        Incrementa o contador de tentativas de login falhas para um usuário.
        """
        conn = await get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE users
                    SET failed_login_attempts = failed_login_attempts + 1
                    WHERE id = %s
                    """,
                    (user_id,)
                )
                await conn.commit()
        finally:
            release_connection(conn)
        
            
    async def lock_account(self, user_id: int, lock_until: str) -> None: # Responsável por bloquear a conta de um usuário até uma data/hora específica.
        """
        Bloqueia a conta de um usuário até uma data/hora específica.
        """
        conn = await get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE users
                    SET locked_until = %s
                    WHERE id = %s
                    """,
                    (lock_until, user_id)
                )
                await conn.commit()
        finally:
            release_connection(conn)
            
        
    async def reset_failed_login_attempts(self, user_id: int) -> None: # Responsável por resetar o contador de tentativas de login falhas para um usuário.
        """
        Reseta o contador de tentativas de login falhas para um usuário.
        """
        conn = await get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE users
                    SET failed_login_attempts = 0
                    WHERE id = %s
                    """,
                    (user_id,)
                )
                await conn.commit()
        finally:
            release_connection(conn)

    async def save_verification_token(self, user_id: int, token: str) -> None:
        """
        Salva o token de verificação de email no usuário.
        """
        conn = await get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE users
                    SET verification_token = %s
                    WHERE id = %s
                    """,
                    (token, user_id)
                )
                await conn.commit()
        finally:
            release_connection(conn)

    async def update_password(self, user_id: int, password_hash: str) -> None:
        """
        Atualiza a senha do usuário e registra a data da alteração.
        """
        conn = await get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE users
                    SET password_hash = %s,
                        password_changed_at = NOW()
                    WHERE id = %s
                    """,
                    (password_hash, user_id)
                )
                await conn.commit()
        finally:
            release_connection(conn)
            
    async def deactivate_user(self, user_id: int) -> None:
        """
        Desativa a conta de um usuário.
        """
        conn = await get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE users
                    SET is_active = FALSE 
                    WHERE id = %s
                    """,
                    (user_id,)
                )
                await conn.commit()
        finally:
            release_connection(conn)  
            
            
    async def update_profile(self, user_id: int, name: str | None = None, email: str | None = None) -> None:
        """
        Atualiza o perfil do usuário.
        """
        conn = await get_connection()

        try:
            async with conn.cursor() as cursor:
                if name and email:
                    await cursor.execute(
                        """
                        UPDATE users
                        SET name = %s, email = %s
                        WHERE id = %s
                        """,
                        (name, email, user_id)
                    )
                elif name:
                    await cursor.execute(
                        """
                        UPDATE users
                        SET name = %s
                        WHERE id = %s
                        """,
                        (name, user_id)
                    )
                elif email:
                    await cursor.execute(
                        """
                        UPDATE users
                        SET email = %s
                        WHERE id = %s
                        """,
                        (email, user_id)
                    )
                await conn.commit()
        finally:
            release_connection(conn)

    async def verify_user(self, user_id: int) -> None:
        """
        Marca o usuário como verificado e limpa o token de verificação.
        """
        conn = await get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE users
                    SET is_verified = TRUE,
                        verification_token = NULL
                    WHERE id = %s
                    """,
                    (user_id,)
                )
                await conn.commit()
        finally:
            release_connection(conn)
