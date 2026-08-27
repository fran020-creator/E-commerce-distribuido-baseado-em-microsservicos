from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt

from .database import Base, engine, SessionLocal
from .models import User
from .schemas import UserCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service",
    description="Serviço de autenticação do e-commerce",
    version="1.0.0",
)



def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


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


@app.post("/auth/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado",
        )

    password_hash = bcrypt.hashpw(
    user.password.encode("utf-8"),
    bcrypt.gensalt(),
).decode("utf-8")

    new_user = User(
        email=user.email,
        password_hash=password_hash,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
    }