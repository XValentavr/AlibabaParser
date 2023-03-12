from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship

from src.models.base_model import BaseModel


class MostSimilarModel(BaseModel):
    __tablename__ = "most_similar"

    amazon_source = relationship('alibaba_source', foreign_keys='alibaba_source.id')
    alibaba_source = relationship('alibaba_source', foreign_keys='alibaba_source.id')
    similarity = Column(Float, nullable=False)
