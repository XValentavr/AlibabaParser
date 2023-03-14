import uuid
from typing import List
from uuid import UUID

from create_engine import session
from cruds.similiraty_cruds import SimilarityCRUDS
from helpers.dtos.most_similar_dto import MostSimilarDTO
from models.alibaba_source_model import AlibabaSourceModel
from models.amazon_source_model import AmazonSourceModel
from models.most_similar_model import MostSimilarModel


class ResultSimilarityCRUDS:

    def __init__(self):
        self.__similarity_cruds = SimilarityCRUDS()

    @staticmethod
    def insert_result_similarity(
            amazon_product_id: UUID, alibaba_product_id: UUID, similarity: float
    ):
        most_similar_id = uuid.uuid4()

        alibaba_product = MostSimilarModel(
            id=most_similar_id,
            alibaba_source_id=alibaba_product_id,
            amazon_source_id=amazon_product_id,
            similarity=similarity,
        )
        session.add(alibaba_product)
        session.commit()

    @staticmethod
    def remove_result_similarity(similarity_id: UUID):
        return (
            session.query(MostSimilarModel)
            .filter(MostSimilarModel.id == similarity_id)
            .delete()
        )

    @staticmethod
    def get_result_similarity_by_id(similarity_id: UUID) -> MostSimilarModel:
        return (
            session.query(MostSimilarModel)
            .filter(MostSimilarModel.id == similarity_id)
            .first()
        )

    def get_most_similar_alibaba_links(self) -> MostSimilarModel:
        base_similarity = self.__similarity_cruds.get_similarity()
        return (
            session.query(MostSimilarModel)
            .join(AmazonSourceModel, AmazonSourceModel.id == MostSimilarModel.amazon_source_id)
            .join(AlibabaSourceModel, AlibabaSourceModel.id == MostSimilarModel.alibaba_source_id)
            .filter(MostSimilarModel.similarity >= base_similarity)
            .first()
        )
