from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class ProductKeywords(BaseModel):
    __tablename__ = "product_keywords"

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

    list_of_keywords = Column(JSONB, nullable=False)
