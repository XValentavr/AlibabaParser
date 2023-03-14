import uuid
from uuid import UUID

from create_engine import session
from models.most_similar_model import MostSimilarModel


class ResultSimilarityCRUDS:
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
