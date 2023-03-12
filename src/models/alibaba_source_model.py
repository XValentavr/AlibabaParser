from sqlalchemy import Column, String

from src.models.base_model import BaseModel


class AlibabaSourceModel(BaseModel):
    __tablename__ = "alibaba_source"

    link = Column(String, nullable=True)

    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    min_price = Column(String, nullable=True)
    max_price = Column(String, nullable=True)
    rrp_price = Column(String, nullable=True)
