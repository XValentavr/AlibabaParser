from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.models.base_model import BaseModel


class AmazonSourceModel(BaseModel):
    __tablename__ = "amazon_source"

    link = Column(String, nullable=True)

    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    price = Column(String, nullable=True)
    rrp_price = Column(String, nullable=True)

    alibaba_source = relationship('AlibabaSourceModel', backref ="amazon_source")
    alibaba_source_id = Column(UUID(as_uuid=True), ForeignKey('alibaba_source.id', ondelete='CASCADE'), nullable=True)

    images = relationship('URLModel', backref ="amazon_source")
    videos = relationship('VideosModel', backref ="amazon_source")
