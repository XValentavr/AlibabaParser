from typing import Optional, List
from uuid import UUID

from create_engine import session
from models.product_keywords import ProductKeywords


class ProductKeywordsCRUDS:
    @staticmethod
    def insert_keywords(list_of_keywords: List, amazon_id: Optional[UUID] = None, alibaba_id: Optional[UUID] = None):
        keywords = ProductKeywords(
            list_of_keywords=list(set(list_of_keywords)), alibaba_source_id=alibaba_id, amazon_source_id=amazon_id
        )
        session.add(keywords)
        session.commit()
