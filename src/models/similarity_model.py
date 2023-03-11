from sqlalchemy import Column, Float

from src.models.base_model import BaseModel


class Similarity(BaseModel):
    __tablename__ = "similarity"

    similarity = Column(Float, nullable=False, default=0.9)
