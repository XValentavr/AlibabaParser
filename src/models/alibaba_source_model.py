from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.models.base_model import BaseModel


class AlibabaSourceModel(BaseModel):
    __tablename__ = "alibaba_source"

    link = Column(String, nullable=True)

    images = relationship('urls', foreign_keys='urls.id')

    images_id = Column(UUID(as_uuid=True), ForeignKey('urls.id'), nullable=False)

    amazon_source = relationship('amazon_source', foreign_keys='amazon_source.id')

    amazon_source_id = Column(UUID(as_uuid=True), ForeignKey('amazon_source.id'), nullable=False)
