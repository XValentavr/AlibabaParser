from typing import List

from cruds.alibaba_cruds import AlibabaCRUDS
from cruds.amazon_cruds import AmazonCRUDS
from cruds.result_similarity_cruds import ResultSimilarityCRUDS
from exceptions.api_exception import APIException
from helpers.dtos.most_similar_dto import MostSimilarDTO
from helpers.init_logger import create_logger


class DatabaseClient:
    def __init__(self):
        self.__result_similarity_cruds = ResultSimilarityCRUDS()
        self.__logger = create_logger()
        self.__amazon_cruds = AmazonCRUDS()
        self.__alibaba_cruds = AlibabaCRUDS()

    def send_most_similar_products(self) -> List:
        try:
            similarity = self.__result_similarity_cruds.get_most_similar_alibaba_links()

            if similarity:
                return [MostSimilarDTO(id=similar.id,
                                       alibaba_source_id=similar.alibaba_source.id,
                                       amazon_source_id=similar.amazon_source.id,
                                       alibaba_source_link=similar.alibaba_source.link,
                                       amazon_source_link=similar.amazon_source.link,
                                       similarity=similar.similarity).dict(by_alias=True) for similar in similarity]
            raise APIException(
                "send_most_similar_products",
                "No similarity found",
                403,
            )
        except Exception as error:
            self.__logger.error(error)
            raise APIException(
                "send_most_similar_products",
                "An error occurred",
                403,
            )

    def clear_amazon_table(self):
        self.__amazon_cruds.remove_amazon_product_all()

    def clear_alibaba_table(self):
        self.__alibaba_cruds.remove_alibaba_product_all()


database_client = DatabaseClient()
