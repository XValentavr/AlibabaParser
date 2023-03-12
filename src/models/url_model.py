from sqlalchemy import Column, String

from src.models.base_model import BaseModel


class URLModel(BaseModel):
    __tablename__ = "urls"

    link = Column(String, nullable=True)
