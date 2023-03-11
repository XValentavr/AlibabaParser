from sqlalchemy import Column, String

from src.models.base_model import BaseModel


class AmazonAndAlibaba(BaseModel):
    __tablename__ = "amazon_alibaba"

    amazon_image_url = Column(String, nullable=True)
    alibaba_image_url = Column(String, nullable=True)
