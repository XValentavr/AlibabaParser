from typing import Optional
from uuid import UUID

from create_engine import session
from src.models.url_model import URLModel


class UrlsCRUDS:
    @staticmethod
    def insert_many_images(link: str, amazon_id: Optional[UUID] = None, alibaba_id: Optional[UUID] = None):
        urls = URLModel(
            link=link, alibaba_product_id=alibaba_id, amazon_product_id=amazon_id
        )
        session.add(urls)
        session.commit()
