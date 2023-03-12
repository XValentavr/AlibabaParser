from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.models.base_model import BaseModel


class AmazonSourceModel(BaseModel):
    __tablename__ = "amazon_source"

    link = Column(String, nullable=True)

    images = relationship('urls', foreign_keys='urls.id')

    images_id = Column(UUID(as_uuid=True), ForeignKey('urls.id'), nullable=False)

    alibaba_source = relationship('alibaba_source', foreign_keys='alibaba_source.id')

    alibaba_source_id = Column(UUID(as_uuid=True), ForeignKey('alibaba_source.id'), nullable=False)
