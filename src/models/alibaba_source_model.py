from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.models.base_model import BaseModel


class AlibabaSourceModel(BaseModel):
    __tablename__ = "alibaba_source"

    link = Column(String, nullable=True)

    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    price = Column(String, nullable=True)
    rrp_price = Column(String, nullable=True)
