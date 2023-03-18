import uuid
from typing import List

from create_engine import session
from cruds.urls_cruds import UrlsCRUDS
from models.alibaba_source_model import AlibabaSourceModel
from models.product_keywords import ProductKeywords
from models.url_model import URLModel


class AlibabaCRUDS:
    def __init__(self):
        self.__url_cruds = UrlsCRUDS()

    def update_alibaba_product_by_id(
            self,
            product_id: uuid.UUID,
            description: str = None,
            min_price: str = None,
            max_price: str = None,
            rrp_price: str = None,
            images: str = None,
    ):
        prod_id = self.__get_alibaba_product_by_id(product_id)

        prod_id.description = description if description else prod_id.description
        prod_id.min_price = min_price if min_price else prod_id.min_price
        prod_id.max_price = max_price if max_price else prod_id.max_price
        prod_id.rrp_price = rrp_price if rrp_price else prod_id.rrp_price
        if images:
            self.__url_cruds.insert_many_images(link=images, alibaba_id=product_id)

    @staticmethod
    def __get_alibaba_product_by_id(product_id: uuid.UUID) -> AlibabaSourceModel:
        return (
            session.query(AlibabaSourceModel)
            .filter(AlibabaSourceModel.id == product_id)
            .first()
        )

    @staticmethod
    def insert_alibaba_products(title: str = None, link: str = None):
        alibaba_id = uuid.uuid4()

        alibaba_product = AlibabaSourceModel(id=alibaba_id, title=title, link=link)
        session.add(alibaba_product)
        session.commit()
        return alibaba_id

    @staticmethod
    def get_alibaba_product_photo_by_id(product_id: uuid.UUID) -> List[URLModel]:
        return (
            session.query(URLModel)
            .filter(URLModel.alibaba_product_id == product_id)
            .all()
        )

    @staticmethod
    def get_alibaba_product_keywords(product_id: uuid.UUID) -> List[ProductKeywords]:
        return (
            session.query(ProductKeywords)
            .filter(ProductKeywords.alibaba_source_id == product_id)
            .all()
        )

    @staticmethod
    def remove_alibaba_product_by_id(product_id):
        return (
            session.query(AlibabaSourceModel)
            .filter(AlibabaSourceModel.id == product_id)
            .delete()
        )

    @staticmethod
    def remove_alibaba_product_all():
        return (
            session.query(AlibabaSourceModel)
            .delete()
        )
