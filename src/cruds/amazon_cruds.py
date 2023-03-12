import uuid
from typing import Optional

from create_engine import session
from src.cruds.urls_cruds import UrlsCRUDS
from src.models.amazon_source_model import AmazonSourceModel
from src.models.url_model import URLModel


class AmazonCRUDS:
    def __init__(self):
        self.__url_cruds = UrlsCRUDS()

    def update_amazon_product_by_id(
            self,
            product_id: uuid.UUID,
            description: str = None,
            min_price: str = None,
            max_price: str = None,
            rrp_price: str = None,
            images: str = None,
    ):
        prod_id = self.__get_amazon_product_by_id(product_id)

        prod_id.description = description if description else prod_id.description
        prod_id.min_price = min_price if min_price else prod_id.min_price
        prod_id.max_price = max_price if max_price else prod_id.max_price
        prod_id.rrp_price = rrp_price if rrp_price else prod_id.rrp_price

        session.commit()

        if images:
            self.__url_cruds.insert_many_images(link=images, amazon_id=product_id)

    @staticmethod
    def __get_amazon_product_by_id(product_id: uuid.UUID) -> AmazonSourceModel:
        return (
            session.query(AmazonSourceModel)
            .filter(AmazonSourceModel.id == product_id)
            .first()
        )

    @staticmethod
    def insert_amazon_products(title: Optional[str] = None, link: Optional[str] = None):
        amazon_id = uuid.uuid4()

        alibaba_product = AmazonSourceModel(id=amazon_id, title=title, link=link)
        session.add(alibaba_product)
        session.commit()
        return amazon_id

    @staticmethod
    def get_amazon_product_photo_by_id(product_id: uuid.UUID) -> list[URLModel]:
        return (
            session.query(URLModel)
            .filter(URLModel.amazon_product_id == product_id)
            .all()
        )

    @staticmethod
    def get_amazon_product_with_alibaba():
        ...

    @staticmethod
    def remove_amazon_product_by_id(product_id: uuid.UUID):
        return (session.query(AmazonSourceModel)
                .filter(AmazonSourceModel.id == product_id).delete())
