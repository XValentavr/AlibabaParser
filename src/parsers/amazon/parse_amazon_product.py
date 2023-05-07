from typing import Optional
from uuid import UUID

from cruds.amazon_cruds import AmazonCRUDS
from cruds.product_keywords_cruds import ProductKeywordsCRUDS
from parsers.amazon.base_parser import BaseParser


class ParseAmazonProduct(BaseParser):
    """
    Class to parse amazon product data from API
    """

    def __init__(self, response):
        # maybe we need it
        super().__init__()
        self.__full_product = response
        self.__product_base_info = response.get("product")

        self.__amazon_cruds = AmazonCRUDS()
        self.__keywords_cruds = ProductKeywordsCRUDS()

    def parse_full_data(self) -> Optional[UUID]:
        """
        main function to work with parser
        :return: product UUID
        """
        if self.__product_base_info:
            return self.__get_product_all_info()

        return None

    def __get_product_all_info(self) -> UUID:
        """
        get all needed product info from API
        :return: product UUID
        """

        title = self.__product_base_info.get("title")
        link = self.__product_base_info.get("link")

        # get all need data
        product_id = self.__amazon_cruds.insert_amazon_products(title=title, link=link)

        self.get_photo_and_videos_if_exists(
            self.__product_base_info, amazon_id=product_id
        )

        self.__get_buybox(product_id)

        self.__get_description(product_id)

        self.__get_keywords(product_id)

        return product_id

    def __get_buybox(self, product_id: UUID) -> None:
        """
        Get amazon min price, max price, rrp price
        :param product_id: amazon product UUID
        :return: None
        """
        buybox_winner = self.__product_base_info.get("buybox_winner")
        if buybox_winner:
            price = buybox_winner.get("price")
            if price:
                self.__amazon_cruds.update_amazon_product_by_id(
                    product_id=product_id,
                    min_price=f"{price.get('value')}{price.get('symbol')}",
                )

            rrp_price = buybox_winner.get("rrp")

            if rrp_price:
                self.__amazon_cruds.update_amazon_product_by_id(
                    product_id=product_id,
                    rrp_price=f"{rrp_price.get('value')}{rrp_price.get('symbol')}",
                )

    def __get_description(self, product_id: UUID) -> None:
        """
        Insert product keywords got from title
        :param product_id: amazon product UUID
        :return: title of product
        """
        description = self.__product_base_info.get("description")
        if description:
            self.__amazon_cruds.update_amazon_product_by_id(
                product_id=product_id, description=description
            )

    def __get_keywords(self, product_id: UUID) -> None:
        """
        Get amazon product price
        :param product_id: amazon product UUID
        :return: None
        """
        keywords = self.__product_base_info.get("keywords_list")
        if keywords:
            self.__keywords_cruds.insert_keywords(
                amazon_id=product_id, list_of_keywords=keywords
            )
