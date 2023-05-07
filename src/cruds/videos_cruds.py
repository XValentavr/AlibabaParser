from typing import Optional
from uuid import UUID

from create_engine import session
from models.videos_model import VideosModel


class VideosCRUDS:
    """
    Class to insert product videos
    """

    @staticmethod
    def insert_many_videos(
        link: str, amazon_id: Optional[UUID] = None, alibaba_id: Optional[UUID] = None
    ):
        """
        insert alibaba or amazon videos to database
        :param link: link of video
        :param amazon_id: amazon UUID of product
        :param alibaba_id: alibaba UUID of product
        :return: None
        """
        urls = VideosModel(
            videos=link, alibaba_product_id=alibaba_id, amazon_product_id=amazon_id
        )
        session.add(urls)
        session.commit()
