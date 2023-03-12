from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base_model import BaseModel


class AmazonSourceModel(BaseModel):
    __tablename__ = "amazon_source"

    link = Column(String, nullable=True)
    images = relationship('urls', foreign_keys='urls.id')
    alibaba_source = relationship('alibaba_source', foreign_keys='alibaba_source.id')
