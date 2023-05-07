from typing import Optional, List
from uuid import UUID

from create_engine import session
from helpers.enums.alibaba.search_types import SearchTypes
from models.alibaba_product_ids import AlibabaProductIdsModel


class AlibabaProductIdsCRUDS:
    @staticmethod
    def insert_product_id(
            product_id: str,
            amazon_id: Optional[UUID] = None,
            alibaba_id: Optional[UUID] = None,
            from_where: SearchTypes = None
    ):
        """
        Function to insert specific product to database
        :param product_id: alibaba id extracted from alibaba url
        :param amazon_id: unique alibaba UUID with which we work in current session
        :param alibaba_id: unique amazon UUID with which we work in current session
        :param from_where: text or image
        :return: None
        """
        product_id = AlibabaProductIdsModel(
            product_id=product_id,
            alibaba_product_id=alibaba_id,
            amazon_product_id=amazon_id,
            from_where=from_where
        )
        session.add(product_id)
        session.commit()

    @staticmethod
    def get_alibaba_products_ids_by_amazon_product_id(
            amazon_id: UUID,
            from_where: SearchTypes
    ) -> List[AlibabaProductIdsModel]:
        """
        Extract from database alibaba product based on amazon product id
        :param amazon_id: amazon product UUID to find alibaba product
        :param from_where: api or text
        :return: list of existing alibaba products
        """
        return (
            session.query(AlibabaProductIdsModel)
            .filter(AlibabaProductIdsModel.amazon_product_id == amazon_id)
            .filter(AlibabaProductIdsModel.from_where == from_where)
            .all()
        )
