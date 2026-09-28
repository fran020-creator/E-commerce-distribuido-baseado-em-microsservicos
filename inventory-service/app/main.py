from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
import httpx

from .database import Base, engine, SessionLocal
from .models import Inventory
from .schemas import InventoryCreate, InventoryUpdate, InventoryResponse


PRODUCT_SERVICE_URL = "http://product-service:8001"

app = FastAPI(
    title="Inventory Service",
    description="Serviço de estoque do e-commerce",
    version="1.0.0",
)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_product(product_id: int):
    try:
        response = httpx.get(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}",
            timeout=5.0,
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Product Service indisponível",
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Erro ao consultar Product Service",
        )

    return response.json()


@app.get("/")
def root():
    return {
        "service": "inventory-service",
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


@app.post("/inventory", response_model=InventoryResponse)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db),
):
    existing_inventory = (
        db.query(Inventory)
        .filter(Inventory.product_id == inventory.product_id)
        .first()
    )

    if existing_inventory:
        raise HTTPException(
            status_code=400,
            detail="Estoque para este produto já existe",
        )
    get_product(inventory.product_id)

    new_inventory = Inventory(
        product_id=inventory.product_id,
        quantity=inventory.quantity,
    )

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    return new_inventory


@app.get("/inventory", response_model=list[InventoryResponse])
def get_inventory(
    db: Session = Depends(get_db),
):
    inventory = db.query(Inventory).all()

    return inventory


@app.get("/inventory/{product_id}", response_model=InventoryResponse)
def get_inventory_by_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    inventory = (
        db.query(Inventory)
        .filter(Inventory.product_id == product_id)
        .first()
    )

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Estoque não encontrado",
        )

    return inventory


@app.put("/inventory/{product_id}", response_model=InventoryResponse)
def update_inventory(
    product_id: int,
    inventory_data: InventoryUpdate,
    db: Session = Depends(get_db),
):
    inventory = (
        db.query(Inventory)
        .filter(Inventory.product_id == product_id)
        .first()
    )

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Estoque não encontrado",
        )

    inventory.quantity = inventory_data.quantity

    db.commit()
    db.refresh(inventory)

    return inventory


@app.delete("/inventory/{product_id}")
def delete_inventory(
    product_id: int,
    db: Session = Depends(get_db),
):
    inventory = (
        db.query(Inventory)
        .filter(Inventory.product_id == product_id)
        .first()
    )

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Estoque não encontrado",
        )

    db.delete(inventory)
    db.commit()

    return {
        "message": "Estoque excluído com sucesso",
        "product_id": product_id,
    }