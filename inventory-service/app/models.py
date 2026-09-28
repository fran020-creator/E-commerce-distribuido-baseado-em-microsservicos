from sqlalchemy import Column, Integer

from .database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, unique=True)
    quantity = Column(Integer, nullable=False, default=0)