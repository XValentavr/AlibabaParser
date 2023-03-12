from uuid import UUID

from create_engine import session
from src.models.videos_model import VideosModel


class VideosCRUDS:

    @staticmethod
    def insert_many_videos(link: str, amazon_id: UUID = None, alibaba_id: UUID = None):
        urls = VideosModel(videos=link, alibaba_product_id=alibaba_id, amazon_product_id=amazon_id)
        session.add(urls)
        session.commit()
