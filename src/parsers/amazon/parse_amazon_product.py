from uuid import UUID

from src.cruds.amazon_cruds import AmazonCRUDS
from src.parsers.amazon.base_parser import BaseParser


class ParseAmazonProduct(BaseParser):
    def __init__(self, response):
        # maybe we need it
        super().__init__()
        self.__full_product = response

        self.__product_base_info = response.get("product")
        self.__amazon_cruds = AmazonCRUDS()

    def parse_full_data(self):
        self.__get_product_all_info()

    def __get_product_all_info(self):
        title = self.__product_base_info.get("title")
        link = self.__product_base_info.get("link")

        # get all need data
        product_id = self.__amazon_cruds.insert_amazon_products(title=title, link=link)

        self.get_photo_and_videos_if_exists(self.__product_base_info, amazon_id=product_id)

        self.__get_buybox(product_id)

        self.__get_description(product_id)

    def __get_buybox(self, product_id: UUID) -> None:
        product = self.__product_base_info.get("buybox_winner")
        price = product.get("price")

        self.__amazon_cruds.update_amazon_product_by_id(product_id=product_id,
                                                        price=f"{price.get('value')}{price.get('symbol')}")
        rrp_price = product.get("rrp")

        self.__amazon_cruds.update_amazon_product_by_id(product_id=product_id,
                                                        rrp_price=f"{rrp_price.get('value')}{rrp_price.get('symbol')}")

    def __get_description(self, product_id: UUID) -> None:
        description = self.__product_base_info.get("description")

        self.__amazon_cruds.update_amazon_product_by_id(product_id=product_id,
                                                        description=description)
