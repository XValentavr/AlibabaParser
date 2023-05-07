from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from models.amazon_source_model import AmazonSourceModel
from models.base_model import BaseModel


class AveragePriceModel(BaseModel):

    __tablename__ = "average_price"

    average = Column(String, nullable=True)

    amazon_product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("amazon_source.id", ondelete="CASCADE"),
        nullable=True,
        unique=False,
    )

    amazon_product = relationship(AmazonSourceModel, backref="average_price")
