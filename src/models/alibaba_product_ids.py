from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from models.alibaba_source_model import AlibabaSourceModel
from models.amazon_source_model import AmazonSourceModel
from models.base_model import BaseModel


class AlibabaProductIdsModel(BaseModel):
    __tablename__ = "alibaba_product_ids"

    product_id = Column(String, nullable=True)

    alibaba_product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("alibaba_source.id", ondelete="CASCADE"),
        nullable=True,
        unique=False,
    )

    alibaba_product = relationship(AlibabaSourceModel, backref="amazon_product_ids")

    amazon_product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("amazon_source.id", ondelete="CASCADE"),
        nullable=True,
        unique=False,
    )
    from_where = Column(String, nullable=True)

    amazon_product = relationship(AmazonSourceModel, backref="amazon_product_ids")
