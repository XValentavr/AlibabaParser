from typing import Optional
from uuid import UUID

from create_engine import session
from models.url_model import URLModel


class UrlsCRUDS:
    """
    Class to insert alibaba or amazon product images
    """

    @staticmethod
    def insert_many_images(
        link: str, amazon_id: Optional[UUID] = None, alibaba_id: Optional[UUID] = None
    ):
        """
        insert alibaba or amazon images to database
        :param link: link of image
        :param amazon_id: amazon UUID of product
        :param alibaba_id: alibaba UUID of product
        :return: None
        """
        urls = URLModel(
            link=link, alibaba_product_id=alibaba_id, amazon_product_id=amazon_id
        )
        session.add(urls)
        session.commit()
