from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from models.base_model import BaseModel


class AmazonSourceModel(BaseModel):
    __tablename__ = "amazon_source"

    link = Column(String, nullable=True)

    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    min_price = Column(String, nullable=True)
    max_price = Column(String, nullable=True)
    rrp_price = Column(String, nullable=True)

    alibaba_source = relationship("AlibabaSourceModel", backref="amazon_source")
    alibaba_source_id = Column(
        UUID(as_uuid=True),
        ForeignKey("alibaba_source.id", ondelete="CASCADE"),
        nullable=True,
    )
