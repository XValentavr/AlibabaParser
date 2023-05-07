import functools
from uuid import UUID

from clients.alibaba.api.alibaba_search_by_api_client import AlibabaSearchByApiClient
from clients.alibaba.api.alibaba_selenium_get_ids import AlibabaSeleniumGetIds
from cruds.alibaba_product_ids_cruds import AlibabaProductIdsCRUDS
from helpers.async_helper import run_in_threadpool
from helpers.enums.alibaba.search_types import SearchTypes


class AlibabaSearchByAPI:
    """
    Class that handle endpoint and alibaba api client
    """

    def __init__(self):
        self.__alibaba_product_ids = AlibabaProductIdsCRUDS()

    @staticmethod
    def get_products_by_images(amazon_product_id: UUID):
        """
        Get alibaba product using API
        :param amazon_product_id: already checked amazon product UUID
        :return: list of alibaba product UUIDs
        """
        # extract url
        alibaba_get_product_from_url = AlibabaSeleniumGetIds(amazon_product_id)
        alibaba_get_product_from_url.search_by_upload_photo(from_where=SearchTypes.PHOTO)  # type:ignore

        # get data from api
        alibaba_search_by_api_client = AlibabaSearchByApiClient(amazon_product_id)
        async_response = functools.partial(alibaba_search_by_api_client.make_api_request, from_where=SearchTypes.PHOTO)
        return run_in_threadpool(funcs=[async_response], raise_on_first_exception=True)[0]

    @staticmethod
    def get_products_by_text(amazon_product_id: UUID, text: str):
        """
        This help methods add possibility to search data from alibaba by text
        :param amazon_product_id: already checked amazon product UUID
        :param text: text to search by
        :return: list of alibaba product UUIDs
        """
        alibaba_search_by_api_client = AlibabaSearchByApiClient(amazon_product_id)
        return alibaba_search_by_api_client.make_api_request_by_text(text=text)


alibaba_search_by_api = AlibabaSearchByAPI()
