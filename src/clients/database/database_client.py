from cruds.result_similarity_cruds import ResultSimilarityCRUDS
from exceptions.api_exception import APIException
from helpers.dtos.most_similar_dto import MostSimilarDTO


class DatabaseClient:
    def __init__(self):
        self.__result_similarity_cruds = ResultSimilarityCRUDS()

    def send_most_similar_products(self) -> dict:
        similarity = self.__result_similarity_cruds.get_most_similar_alibaba_links()

        if similarity:
            most_similar_dto = MostSimilarDTO(id=similarity.id,
                                              alibaba_source_id=similarity.alibaba_source.id,
                                              amazon_source_id=similarity.amazon_source.id,
                                              alibaba_source_link=similarity.alibaba_source.link,
                                              amazon_source_link=similarity.amazon_source.link,
                                              similarity=similarity.similarity).dict(by_alias=True)
            return most_similar_dto

        raise APIException(
            "send_most_similar_products",
            "No similarity found",
            403,
        )


database_client = DatabaseClient()
