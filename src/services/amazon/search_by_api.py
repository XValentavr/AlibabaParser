from typing import Union
from uuid import UUID

from clients.amazon.api.amazon_rainforest_api import AmazonRainforestAPI

from helpers.validators.get_asin_from_url import get_asin_from_url


class AmazonRainforestAPIService:
    """
    Class to work with rainforest API to get amazon product data
    """

    @staticmethod
    def get_products(url: str) -> Union[UUID, None]:
        """
        Get amazon product info using rainforest API
        :param url: url to work with. Contains asin
        :return: amazon product UUID
        """
        asin = get_asin_from_url(url)

        if asin:
            amazon_rainforest_api = AmazonRainforestAPI(asin, domain=None)

            return amazon_rainforest_api.get_product_full_info()
        raise Exception('No asin found, try again')


amazon_search_by_rainforest_api = AmazonRainforestAPIService()
