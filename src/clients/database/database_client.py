import logging
from typing import List
from uuid import UUID

from cruds.alibaba_cruds import AlibabaCRUDS
from cruds.amazon_cruds import AmazonCRUDS
from cruds.result_similarity_cruds import ResultSimilarityCRUDS
from exceptions.api_exception import APIException
from helpers.calculate_average_price import calculate_average_price
from helpers.dtos.most_similar_dto import MostSimilarDTO
from helpers.init_logger import create_logger


class DatabaseClient:
    """
    Class to work with database
    """

    def __init__(self):
        self.__result_similarity_cruds = ResultSimilarityCRUDS()
        self.__logger = create_logger()
        self.__amazon_cruds = AmazonCRUDS()
        self.__alibaba_cruds = AlibabaCRUDS()

    def send_most_similar_products(self, amazon_product_id: UUID) -> List:
        """
        This function send to frontend list of most similar products after all checking
        :return: list of most similar products
        """
        try:
            similarity = self.__result_similarity_cruds.get_most_similar_alibaba_links(amazon_product_id)

            if similarity:
                res_list = [
                    MostSimilarDTO(
                        id=similar.id,
                        alibaba_source_id=similar.alibaba_source.id,
                        amazon_source_id=similar.amazon_source.id,
                        alibaba_source_link=similar.alibaba_source.link,
                        amazon_source_link=similar.amazon_source.link,
                        similarity=similar.similarity,
                    ).dict(by_alias=True)
                    for similar in similarity
                ]
                res_list.append({'average': calculate_average_price.calculator(similar=similarity)})

                return res_list
            return []
            # raise APIException(
            #     "send_most_similar_products",
            #     "No similarity found",
            #     403,
            # )
        except Exception:
            self.__logger.setLevel(logging.DEBUG)
            raise APIException(
                "send_most_similar_products",
                "An error occurred",
                403,
            )

    def clear_amazon_table(self, product_id: UUID):
        """
        Clear all amazon data
        :return: None
        """
        self.__amazon_cruds.remove_amazon_product_by_id(product_id)

    def clear_alibaba_table(self, product_id: UUID):
        """
        Clear all alibaba data
        :return: None
        """
        self.__alibaba_cruds.remove_alibaba_product_by_id(product_id)


database_client = DatabaseClient()
