from sqlalchemy import Column, Float

from models.base_model import BaseModel


class SimilarityModel(BaseModel):
    __tablename__ = "similarity"

    similarity = Column(Float, nullable=False, default=0.9)
