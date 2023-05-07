import uuid
from typing import List
from uuid import UUID

from sqlalchemy import and_

from create_engine import session
from cruds.similiraty_cruds import SimilarityCRUDS
from models.alibaba_source_model import AlibabaSourceModel
from models.amazon_source_model import AmazonSourceModel
from models.most_similar_model import MostSimilarModel


class ResultSimilarityCRUDS:
    """
    Class to work with similar products
    """

    def __init__(self):
        self.__similarity_cruds = SimilarityCRUDS()

    @staticmethod
    def insert_result_similarity(
            amazon_product_id: UUID, alibaba_product_id: UUID, similarity: float
    ):
        """
        Afeter checking similariry insert to database similar product
        :param amazon_product_id: UUID of amazon product
        :param alibaba_product_id: UUID of alibaba product
        :param similarity: rate of similarity between products
        :return: None
        """
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
        """
        Delete product similarity by id
        :param similarity_id: UUID of similarity to remove
        :return: None
        """
        return (
            session.query(MostSimilarModel)
            .filter(MostSimilarModel.id == similarity_id)
            .delete()
        )

    @staticmethod
    def get_result_similarity_by_id(similarity_id: UUID) -> MostSimilarModel:
        """
        Get product similarity by id
        :param similarity_id: UUID of similarity to find
        :return: existing similarity rate of products
        """
        return (
            session.query(MostSimilarModel)
            .filter(MostSimilarModel.id == similarity_id)
            .first()
        )

    @staticmethod
    def get_result_similarity_by_amazon_id(amazon_id: UUID) -> List[MostSimilarModel]:
        """
        Get product similarity by amazon product id
        :param amazon_id: UUID of amazon product to find
        :return: existing similarity rate of products
        """
        return (
            session.query(MostSimilarModel)
            .filter(MostSimilarModel.amazon_source_id == amazon_id)
            .all()
        )

    @staticmethod
    def get_result_similarity_by_alibaba_id(alibaba_id: UUID) -> List[MostSimilarModel]:
        """
        Get product similarity by alibaba product id
        :param alibaba_id: UUID of alibaba product to find
        :return: existing similarity rate of products
        """
        return (
            session.query(MostSimilarModel)
            .filter(MostSimilarModel.alibaba_source_id == alibaba_id)
            .all()
        )

    @staticmethod
    def get_result_similarity_between(
            amazon_product_id: UUID, start_similarity: float, end_similarity: float
    ) -> List[MostSimilarModel]:
        """
        Get result similarity between some similarity rates. Need for additional checking
        :param amazon_product_id: amazon UUID to find
        :param start_similarity: start similarity rate
        :param end_similarity: end similarity rate
        :return: similarity that exists between
        """
        return (
            session.query(AmazonSourceModel, AlibabaSourceModel)
            .join(
                MostSimilarModel,
                AlibabaSourceModel.id == MostSimilarModel.alibaba_source_id,
            )
            .filter(
                and_(
                    MostSimilarModel.similarity.between(
                        start_similarity, end_similarity
                    ),
                    AmazonSourceModel.id == MostSimilarModel.amazon_source_id,
                ).filter(MostSimilarModel.amazon_source_id == amazon_product_id)
            )
            .all()
        )

    @staticmethod
    def get_most_similar_alibaba_links(amazon_product_id: UUID) -> List[MostSimilarModel]:
        """
        Get the most similar product to send to frontend
        :return: list of the most similar amazon ana alibaba products
        """
        return (
            session.query(MostSimilarModel)
            .join(
                AmazonSourceModel,
                AmazonSourceModel.id == MostSimilarModel.amazon_source_id,
            )
            .join(
                AlibabaSourceModel,
                AlibabaSourceModel.id == MostSimilarModel.alibaba_source_id,
            )
            .filter(MostSimilarModel.amazon_source_id == amazon_product_id)
            .all()
        )

    @staticmethod
    def remove_not_similar_products(alibaba_id: UUID, amazon_id: UUID):
        """
        This function removes not similar product after text checking
        :return: none
        """
        result_alibaba = (
            session.query(AlibabaSourceModel)
            .filter(AlibabaSourceModel.id == alibaba_id)
            .delete()
        )
        result_amazon = (
            session.query(AmazonSourceModel)
            .filter(AmazonSourceModel.id == amazon_id)
            .delete()
        )
        return result_alibaba > 1 and result_amazon > 1
