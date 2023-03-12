from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from models.alibaba_source_model import AlibabaSourceModel
from models.amazon_source_model import AmazonSourceModel
from models.base_model import BaseModel


class VideosModel(BaseModel):
    __tablename__ = "videos"

    videos = Column(String, nullable=True)

    alibaba_product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("alibaba_source.id", ondelete="CASCADE"),
        nullable=True,
        unique=False,
    )

    alibaba_product = relationship(AlibabaSourceModel)

    amazon_product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("amazon_source.id", ondelete="CASCADE"),
        nullable=True,
        unique=False,
    )

    amazon_product = relationship(AmazonSourceModel)
