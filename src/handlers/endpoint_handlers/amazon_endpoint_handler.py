from handlers.endpoint_handlers.amazon_endpoint_helper import amazon_endpoint_helper
from helpers.enums.alibaba.search_types import SearchTypes
from helpers.init_logger import create_logger
from services.amazon.search_by_api import amazon_search_by_rainforest_api
from services.amazon.search_by_selenium import amazon_search_by_selenium_service


class AmazonEndpointHandler:
    """
    Class to handle endpoints
    """

    def __init__(self):
        self.__logger = create_logger()

    @staticmethod
    def parse_data(search_type_alibaba: str, search_type_amazon: str, photo: str) -> None:
        """
        main endpoint to get product similarity of alibaba and amazon stores
        :param search_type_alibaba: search type of alibaba (API or Selenium)
        :param search_type_amazon: search type of amazon (API or Selenium)
        :param photo: amazon product url
        :return: list of most similar products
        """
        if search_type_amazon == SearchTypes.API:

            # rainforest api
            amazon_product_id = amazon_search_by_rainforest_api.get_products(photo)
            if amazon_product_id:
                # get alibaba photos by selenium
                amazon_endpoint_helper.products_handler(amazon_product_id, search_type_alibaba)
                return amazon_product_id
            else:
                raise Exception('No product found')

        elif search_type_amazon == SearchTypes.SELENIUM:
            # selenium parser
            amazon_product_id = amazon_search_by_selenium_service.search_by_url(photo)
            amazon_endpoint_helper.products_handler(amazon_product_id, search_type_alibaba)
            return amazon_product_id

        else:
            raise Exception('Method is not found')


amazon_endpoint_handler = AmazonEndpointHandler()
