from fastapi import FastAPI

app = FastAPI(
    title="Auth Service",
    description="Serviço de autenticação do e-commerce",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "service": "auth-service",
        "status": "online",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }