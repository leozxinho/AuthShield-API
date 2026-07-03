# Sistema de Login - API de Autenticação

API de autenticação completa desenvolvida com **FastAPI**, **MySQL** (aiomysql) e **JWT**, seguindo arquitetura em camadas (Controller → UseCase → Repository).

## Tecnologias

- **FastAPI** — Framework web assíncrono
- **MySQL** — Banco de dados relacional (via aiomysql)
- **JWT (python-jose)** — Autenticação por tokens
- **bcrypt (passlib)** — Hash de senhas
- **slowapi** — Rate limiting
- **aiosmtplib** — Envio de emails assíncrono
- **Pydantic** — Validação de dados

## Arquitetura

```
├── app/
│   ├── controller/        # Rotas (endpoints)
│   ├── schemas/           # Validação de entrada (Pydantic)
│   ├── dependencies.py    # Dependências de injeção (auth)
│   └── rate_limiter.py    # Configuração do rate limiter
├── domain/
│   ├── entities/          # Entidades de domínio
│   ├── usecase/           # Regras de negócio
│   └── interfaces/        # Interfaces/contratos
├── infrastructure/
│   ├── config/            # Configurações (.env)
│   ├── database/          # Conexão e criação de tabelas
│   ├── email/             # Serviço de envio de emails
│   ├── repositories/      # Acesso ao banco de dados
│   └── security/          # JWT e Hash
└── main.py                # Ponto de entrada da aplicação
```

## Endpoints

| Método | Rota                    | Protegido | Descrição                         |
|--------|-------------------------|-----------|-----------------------------------|
| POST   | `/auth/login`           | Não       | Login do usuário                  |
| POST   | `/auth/register`        | Não       | Registro de novo usuário          |
| POST   | `/auth/logout`          | Sim       | Logout (revoga token)             |
| GET    | `/auth/verify`          | Não       | Verificação de email              |
| POST   | `/auth/refresh`         | Sim       | Renovação do token de acesso      |
| POST   | `/auth/forgot-password` | Não       | Solicitar redefinição de senha    |
| POST   | `/auth/reset-password`  | Não       | Redefinir senha via token         |
| PUT    | `/auth/change-password` | Sim       | Alterar senha (autenticado)       |
| PUT    | `/auth/profile`         | Sim       | Atualizar perfil                  |
| DELETE | `/auth/account`         | Sim       | Desativar conta                   |

## Regras de Negócio

1. **Bloqueio por tentativas de login** — Após 5 tentativas falhas consecutivas, a conta é temporariamente bloqueada.

2. **Token JWT com expiração** — Access token expira em 15 minutos; refresh token expira em 24 horas.

3. **Verificação de email obrigatória** — Após o registro, o usuário recebe um email com token de verificação (válido por 24h). Não é possível fazer login sem verificar o email.

4. **Rate limiting** — Endpoints públicos (login, register, forgot-password, verify) são limitados a 5 requisições por minuto por IP.

5. **Detecção de login suspeito por IP** — Após login bem-sucedido, se o IP não está na lista de IPs conhecidos do usuário, um email de alerta é enviado.

6. **Log de tentativas de login** — Toda tentativa de login (sucesso ou falha) é registrada com IP, user-agent e timestamp.

7. **Histórico de senhas** — Ao alterar a senha, as últimas 5 senhas são verificadas para impedir reutilização.

8. **Expiração de senha (90 dias)** — Se a senha não é alterada há mais de 90 dias, o usuário é forçado a redefinir.

9. **Validação de senha forte** — A senha deve ter no mínimo 8 caracteres, incluindo: letra maiúscula, número e caractere especial.

10. **Blacklist de tokens (logout)** — Ao fazer logout, o token é adicionado a uma blacklist e não pode mais ser utilizado.

11. **Refresh token com uso único** — Ao utilizar um refresh token, ele é revogado e um novo par (access + refresh) é gerado.

12. **Revalidação de email ao alterar** — Ao trocar o email no perfil, um novo email de confirmação é enviado. O email só é atualizado após verificação.

13. **Desativação de conta** — Ao desativar, a conta é marcada como inativa e todos os refresh tokens são revogados.

14. **Proteção de endpoints por JWT** — Endpoints protegidos utilizam a dependência `get_current_user` que valida o token e retorna o usuário autenticado.

15. **Validação de dados de entrada** — Todos os inputs são validados via schemas Pydantic (email válido, nome apenas letras, senha com critérios).

## Como Executar

### Pré-requisitos

- Python 3.12+
- MySQL

### Instalação

```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd leonardo_sistema_de_login

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Configuração

Criar arquivo `.env` na raiz com as variáveis:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=sistema_login

JWT_SECRET_KEY=sua_chave_secreta
JWT_ALGORITHM=HS256

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app
```

### Executar

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`.

Documentação interativa (Swagger): `http://localhost:8000/docs`

## Tabelas do Banco de Dados

- **users** — Dados do usuário, status de verificação, tentativas de login, bloqueio
- **token_blacklist** — Tokens revogados (logout)
- **refresh_tokens** — Refresh tokens ativos
- **password_history** — Histórico de senhas anteriores
- **login_logs** — Registro de tentativas de login
