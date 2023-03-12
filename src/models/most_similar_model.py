from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.models.base_model import BaseModel


class MostSimilarModel(BaseModel):
    __tablename__ = "most_similar"

    amazon_source = relationship('alibaba_source', foreign_keys='alibaba_source.id')

    amazon_source_id = Column(UUID(as_uuid=True), ForeignKey('amazon_source.id'), nullable=False)

    alibaba_source = relationship('alibaba_source', foreign_keys='alibaba_source.id')

    alibaba_source_id = Column(UUID(as_uuid=True), ForeignKey('alibaba_source.id'), nullable=False)

    similarity = Column(Float, nullable=False)
