from infrastructure.database.connection import get_connection, release_connection


async def create_tables():
    """
    Cria as tabelas no banco de dados MySQL.
    """
    conn = await get_connection()

    try:
        async with conn.cursor() as cursor:
            # Tabela users
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_verified BOOLEAN DEFAULT FALSE,
                    verification_token TEXT NULL,
                    password_changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    failed_login_attempts INT DEFAULT 0,
                    locked_until DATETIME DEFAULT NULL
                )
            """)
            print("Tabela 'users' criada com sucesso.")

            # Tabela token_blacklist
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS token_blacklist (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    token TEXT NOT NULL,
                    expired_at DATETIME NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Tabela 'token_blacklist' criada com sucesso.")

            # Tabela refresh_tokens
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS refresh_tokens (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    token TEXT NOT NULL,
                    is_revoked BOOLEAN DEFAULT FALSE,
                    expires_at DATETIME NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            print("Tabela 'refresh_tokens' criada com sucesso.")

            # Tabela password_history
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS password_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            print("Tabela 'password_history' criada com sucesso.")

            # Tabela login_logs
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS login_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    ip_address VARCHAR(45) NOT NULL,
                    user_agent TEXT,
                    success BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            print("Tabela 'login_logs' criada com sucesso.")

    finally:
        release_connection(conn)
