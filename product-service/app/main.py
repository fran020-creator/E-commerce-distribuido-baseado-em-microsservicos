from fastapi import FastAPI
from sqlalchemy import text

from .database import Base,engine
from .models import Product


app = FastAPI(
    title="Product Service",
    description="Serviço de produtos do e-commerce",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "service": "product-service",
        "status": "online",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/health/database")
def health_database():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }