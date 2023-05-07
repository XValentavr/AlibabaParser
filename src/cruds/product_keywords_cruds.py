from typing import Optional, List
from uuid import UUID

from create_engine import session
from models.product_keywords import ProductKeywords


class ProductKeywordsCRUDS:
    """
    Class to work with alibaba or amazon product keywords
    """

    @staticmethod
    def insert_keywords(
            list_of_keywords: List,
            amazon_id: Optional[UUID] = None,
            alibaba_id: Optional[UUID] = None,
    ):
        """
        Insert alibaba or amazon product keywords
        :param list_of_keywords: list of product keywords
        :param amazon_id: amazon UUID product
        :param alibaba_id: alibaba UUID product
        :return: None
        """
        keywords = ProductKeywords(
            list_of_keywords=list(set(list_of_keywords)),
            alibaba_source_id=alibaba_id,
            amazon_source_id=amazon_id,
        )
        session.add(keywords)
        session.commit()

    @staticmethod
    def get_alibaba_product_keywords(product_id: UUID):
        """
        This function gets keywords from alibaba
        :return: list of keywords
        """
        return (
            session.query(ProductKeywords)
            .filter(ProductKeywords.alibaba_source_id == product_id)
            .first()
        )

    @staticmethod
    def get_amazon_product_keywords(product_id: UUID) -> ProductKeywords:
        """
        This function gets keywords from amazon
        :return: list of keywords
        """
        return (
            session.query(ProductKeywords)
            .filter(ProductKeywords.amazon_source_id == product_id)
            .first()
        )


product_keywords_cruds = ProductKeywordsCRUDS()
