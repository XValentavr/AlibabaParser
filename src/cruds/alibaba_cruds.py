import uuid

from create_engine import session
from src.cruds.urls_cruds import UrlsCRUDS
from src.models.alibaba_source_model import AlibabaSourceModel


class AlibabaCRUDS:
    def __init__(self):
        self.__url_cruds = UrlsCRUDS()

    @staticmethod
    def __get_alibaba_product_by_id(product_id: uuid.UUID) -> AlibabaSourceModel:
        return session.query(AlibabaSourceModel).filter(AlibabaSourceModel.id == product_id).first()

    @staticmethod
    def insert_alibaba_products(title: str, link: str):
        alibaba_id = uuid.uuid4()

        alibaba_product = AlibabaSourceModel(id=alibaba_id, title=title, link=link)
        session.add(alibaba_product)
        session.commit()

    def update_alibaba_product_by_id(self, product_id: uuid.UUID, description: str = None, price: str = None,
                                     rrp_price: str = None, images: list = None):
        prod_id = self.__get_alibaba_product_by_id(product_id)

        prod_id.description = description if description else None
        prod_id.price = price if price else None
        prod_id.rrp_price = rrp_price if price else None

        self.__url_cruds.insert_many_images(images=images, alibaba_id=prod_id.id)

    def get_alibaba_product_with_photo_by_id(self):
        ...

    def get_alibaba_product_with_amazon_by_id(self):
        ...

    def remove_all_alibaba_products(self):
        ...

    def remove_alibaba_product_by_id(self):
        ...
