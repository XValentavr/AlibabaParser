import re
from typing import Optional
from uuid import UUID

from cruds.alibaba_cruds import AlibabaCRUDS
from cruds.alibaba_product_ids_cruds import AlibabaProductIdsCRUDS
from cruds.amazon_cruds import AmazonCRUDS
from helpers.enums.alibaba.search_types import SearchTypes


class AlibabaClientHelper:

    def __init__(self):
        self.__amazon_cruds = AmazonCRUDS()
        self.__alibaba_product_ids = AlibabaProductIdsCRUDS()
        self.__alibaba_cruds = AlibabaCRUDS()

    def insert_alibaba_products(self, goods: list, amazon_product_id: UUID, from_where: SearchTypes):
        """
        Insert alibaba products to table depends on type (celery or sync)
        """
        for good in goods:
            if from_where == SearchTypes.PHOTO:
                url = good.get_attribute("href")
                product_id = self.__extract_product_id(url)
                self.__insert_alibaba_products(url, product_id, amazon_product_id, from_where=from_where)
            elif from_where == SearchTypes.TEXT:
                product_id = good.get('num_iid')
                self.__insert_alibaba_products(None, product_id, amazon_product_id, from_where=from_where)

    @staticmethod
    def __extract_product_id(url: str):
        """
        Using regex get product id from url
        :param url: url to get product id from
        :return: extracted product id
        """
        match = re.search(r"(\d+)\.html", url)

        if match:
            return match.group(1)
        return

    def __insert_alibaba_products(self, url: Optional[str],
                                  product_id: str,
                                  amazon_product_id: UUID,
                                  from_where: SearchTypes):
        """
        handler to add data to table
        """
        alibaba_product_id = self.__alibaba_cruds.insert_alibaba_products(link=url)

        if product_id:
            self.__alibaba_product_ids.insert_product_id(
                from_where=from_where,
                product_id=product_id,
                alibaba_id=alibaba_product_id,
                amazon_id=amazon_product_id,
            )


alibaba_client_helper = AlibabaClientHelper()
