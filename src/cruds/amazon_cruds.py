import uuid

from create_engine import session
from src.cruds.urls_cruds import UrlsCRUDS
from src.models.amazon_source_model import AmazonSourceModel


class AmazonCRUDS:
    def __init__(self):
        self.__url_cruds = UrlsCRUDS()

    @staticmethod
    def __get_amazon_product_by_id(product_id: uuid.UUID) -> AmazonSourceModel:
        return session.query(AmazonSourceModel).filter(AmazonSourceModel.id == product_id).first()

    @staticmethod
    def insert_amazon_products(title: str = None, link: str = None):
        amazon_id = uuid.uuid4()

        alibaba_product = AmazonSourceModel(id=amazon_id, title=title, link=link)
        session.add(alibaba_product)
        session.commit()
        return amazon_id

    def update_amazon_product_by_id(self, product_id: uuid.UUID,
                                    description: str = None,
                                    price: str = None,
                                    rrp_price: str = None):

        prod_id = self.__get_amazon_product_by_id(product_id)

        prod_id.description = description if description else prod_id.description
        prod_id.price = price if price else prod_id.price
        prod_id.rrp_price = rrp_price if price else  prod_id.rrp_price

        session.commit()

    def get_amazon_product_with_photo(self):
        ...

    def get_amazon_product_with_alibaba(self):
        ...

    def remove_all_amazon_product(self):
        ...

    def remove_amazon_product_by_id(self):
        ...
