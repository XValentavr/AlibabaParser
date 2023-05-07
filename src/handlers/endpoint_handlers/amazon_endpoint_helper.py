from typing import List
from uuid import UUID

from ai.data_handlers.data_handler import DataHandler
from helpers.enums.alibaba.search_types import SearchTypes
from helpers.validators.remove_special_symbols import remove_special_symbols
from services.alibaba.search_by_api import alibaba_search_by_api
from services.alibaba.search_by_selenium import alibaba_search_by_selenium
from tasks.celery_alibaba_tasks import celery_alibaba_tasks


class AmazonEndpointHelper:
    """
    helper class for endpoint
    """

    def products_handler(self, amazon_product_id: UUID, search_type_alibaba: str):
        """
        this main method is main between endpoint and services
        :param amazon_product_id: amazon product to get info about
        :param search_type_alibaba: search type to use api or selenium
        :return: None
        """
        text_to_search = remove_special_symbols(self.__create_search_text_from_keywords(amazon_id=amazon_product_id))

        # run celery task
        result = celery_alibaba_tasks.create_text_finder_task.delay(amazon_product_id, text_to_search)
        # continue as usual script
        alibaba_product_ids = self.__get_alibaba_product(amazon_product_id, search_type_alibaba)

        self.aws_trigger(amazon_product_id, alibaba_product_ids)

        # after all check if task is completed
        result.get()

    @staticmethod
    def __get_alibaba_product(amazon_product_id: UUID, search_type_alibaba: str):
        """
        Method to get alibaba product using selenium or api
        :param amazon_product_id: amazon product to build relationship
        :param search_type_alibaba: search type to use api or selenium
        :return: list of alibaba product ids
        """
        if search_type_alibaba == SearchTypes.SELENIUM:
            alibaba_product_ids = (
                alibaba_search_by_selenium.search_by_photo_service(
                    amazon_product_id
                )
            )
        else:
            alibaba_product_ids = alibaba_search_by_api.get_products_by_images(
                amazon_product_id=amazon_product_id
            )

        return alibaba_product_ids

    @staticmethod
    def aws_trigger(amazon_id: UUID, alibaba_ids: List[UUID]):
        """
        Triggers AWS lambda to get similarity
        :param amazon_id: main amazon product
        :param alibaba_ids: found alibaba ids
        :return: None
        """
        data_handler = DataHandler(amazon_id, alibaba_ids)

        data_handler.aws_similarity_images()

    @staticmethod
    def __create_search_text_from_keywords(amazon_id: UUID, ):
        """
        Create text to search alibaba api based on amazon product keywords
        """
        from cruds.product_keywords_cruds import product_keywords_cruds
        keywords = product_keywords_cruds.get_amazon_product_keywords(amazon_id)
        if len(keywords.list_of_keywords) > 5:
            return ' '.join(keywords.list_of_keywords[0:3])
        return ' '.join(keywords.list_of_keywords)


amazon_endpoint_helper = AmazonEndpointHelper()
