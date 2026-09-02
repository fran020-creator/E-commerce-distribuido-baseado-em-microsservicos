# E-Commerce Microservices

Projeto de estudo de uma arquitetura de microsserviços para uma plataforma de e-commerce. Cada serviço é independente, containerizado com Docker e se comunica via rede interna.

## Serviços

| Serviço | Descrição | Status |
|---|---|---|
| `auth-service` | Registro, login e validação de tokens JWT | ✅ Implementado |
| `product-service` | Catálogo de produtos | 🚧 Em desenvolvimento |
| `order-service` | Gestão de pedidos | 🚧 Em desenvolvimento |
| `payment-service` | Processamento de pagamentos | 🚧 Em desenvolvimento |
| `inventory-service` | Controle de estoque | 🚧 Em desenvolvimento |
| `notification-service` | Envio de notificações | 🚧 Em desenvolvimento |
| `gateway` | API Gateway | 🚧 Em desenvolvimento |

## Stack

- **Linguagem:** Python 3.12
- **Framework:** FastAPI
- **Banco de dados:** PostgreSQL 16
- **ORM:** SQLAlchemy
- **Autenticação:** JWT (via `python-jose`)
- **Containerização:** Docker + Docker Compose

## Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose instalados
- Git

## Como rodar

**1. Clone o repositório**

```bash
git clone https://github.com/seu-usuario/ecommerce-microservice.git
cd ecommerce-microservice
```

**2. Configure as variáveis de ambiente**

Copie o arquivo de exemplo e preencha com seus valores:

```bash
cp .env.example .env
```

Edite o `.env`:

```env
JWT_SECRET_KEY=sua-chave-secreta-aqui
```

> Gere uma chave segura com: `openssl rand -hex 32`

**3. Suba os containers**

```bash
docker compose up --build
```

## Endpoints — Auth Service

Base URL: `http://localhost:8000`

### `POST /auth/register`
Cria uma nova conta de usuário.

**Body:**
```json
{
  "email": "usuario@exemplo.com",
  "password": "sua-senha"
}
```

**Resposta `200`:**
```json
{
  "id": 1,
  "email": "usuario@exemplo.com"
}
```

---

### `POST /auth/login`
Autentica o usuário e retorna um token JWT.

**Body:**
```json
{
  "email": "usuario@exemplo.com",
  "password": "sua-senha"
}
```

**Resposta `200`:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

---

### `GET /auth/me`
Retorna os dados do usuário autenticado.

**Header:**
```
Authorization: Bearer <token>
```

**Resposta `200`:**
```json
{
  "id": 1,
  "email": "usuario@exemplo.com"
}
```

---

### `GET /health`
Verifica se o serviço está no ar.

**Resposta `200`:**
```json
{
  "status": "healthy"
}
```

## Documentação interativa

Com os serviços rodando, acesse a documentação automática gerada pelo FastAPI:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Estrutura do projeto

```
ecommerce-microservice/
├── auth-service/
│   ├── app/
│   │   ├── database.py     # Conexão com o banco de dados
│   │   ├── models.py       # Modelos do SQLAlchemy
│   │   ├── schemas.py      # Schemas Pydantic (validação)
│   │   ├── security.py     # Geração e verificação de JWT
│   │   └── main.py         # Rotas e configuração da aplicação
│   ├── Dockerfile
│   └── requirements.txt
├── product-service/
├── order-service/
├── payment-service/
├── inventory-service/
├── notification-service/
├── gateway/
├── docker-compose.yml
├── .env.example
└── README.md
```

## Variáveis de ambiente

| Variável | Descrição | Obrigatório |
|---|---|---|
| `JWT_SECRET_KEY` | Chave secreta para assinar tokens JWT | ✅ |
