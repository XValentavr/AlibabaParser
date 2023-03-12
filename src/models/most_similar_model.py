from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.models.base_model import BaseModel


class MostSimilarModel(BaseModel):
    __tablename__ = "most_similar"

    amazon_source = relationship("AmazonSourceModel", backref="most_similar")

    amazon_source_id = Column(
        UUID(as_uuid=True),
        ForeignKey("amazon_source.id", ondelete="CASCADE"),
        nullable=True,
    )

    alibaba_source = relationship("AlibabaSourceModel", backref="most_similar")

    alibaba_source_id = Column(
        UUID(as_uuid=True),
        ForeignKey("alibaba_source.id", ondelete="CASCADE"),
        nullable=True,
    )

    similarity = Column(Float, nullable=False)
