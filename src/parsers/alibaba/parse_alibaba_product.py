import re
from typing import Dict, Optional
from uuid import UUID

from clients.gpt.GPT import GPTClient
from cruds.alibaba_cruds import AlibabaCRUDS
from cruds.product_keywords_cruds import ProductKeywordsCRUDS


class ParseAlibabaProduct:
    """
    Class to parse alibaba product data from API
    """

    def __init__(self, alibaba_product: Dict):
        self.__product_base_info = alibaba_product.get("item")

        self.__alibaba_cruds = AlibabaCRUDS()
        self.__keywords_cruds = ProductKeywordsCRUDS()
        self.__gpt_client = GPTClient()

    def parse_full_data(self, product_id: UUID):
        """
        main function to work with parser
        :return: product UUID
        """
        return self.__get_product_all_info(product_id)

    def __get_product_all_info(self, product_id: UUID) -> UUID:
        """
        get all needed product info from API
        :return: product UUID
        """
        title = self.__product_base_info.get("title")
        link = self.__product_base_info.get("detail_url")

        # get all need data

        self.__get_photo_and_videos_if_exists(product_id)

        self.__get_price(product_id)

        description = self.__get_keywords(product_id, title=title)

        self.__alibaba_cruds.update_alibaba_product_by_id(
            product_id, description=description, title=title, link=link
        )

        return product_id

    def __get_keywords(self, product_id: UUID, title: Optional[str]):
        """
        Insert product keywords got from title
        :param product_id: alibaba product UUID
        :return: title of product
        """
        if title:
            self.__gpt_client.get_keywords(product_id, text_to_extract=title)

        return title

    def __get_photo_and_videos_if_exists(self, product_id: UUID):
        """
        Insert product image and video if exists
        :param product_id: alibaba product UUID
        :return: None
        """
        for image in self.__product_base_info.get("item_imgs"):
            self.__alibaba_cruds.update_alibaba_product_by_id(
                product_id, images=image.get("url")
            )

        self.__alibaba_cruds.update_alibaba_product_by_id(
            product_id, videos=self.__product_base_info.get("video_url")
        )

    def __get_price(self, product_id: UUID):
        """
        Get alibaba product price
        :param product_id: alibaba product UUID
        :return:
        """
        price_range = self.__product_base_info.get('priceRange')
        if price_range and isinstance(price_range, list):
            min_price = price_range[-1][-1]
            max_price = price_range[0][-1]
            self.__alibaba_cruds.update_alibaba_product_by_id(
                product_id, max_price=max_price, min_price=min_price
            )
        else:
            price = str(self.__product_base_info.get('price'))
            cleaned_price = re.sub(r'[^\w.]+', '', price)
            self.__alibaba_cruds.update_alibaba_product_by_id(
                product_id, max_price=cleaned_price, min_price=cleaned_price
            )
