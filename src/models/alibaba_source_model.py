from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base_model import BaseModel


class AlibabaSourceModel(BaseModel):
    __tablename__ = "alibaba_source"

    link = Column(String, nullable=True)
    images = relationship('urls', foreign_keys='urls.id')
