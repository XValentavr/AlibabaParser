from uuid import UUID

from src.cruds.urls_cruds import UrlsCRUDS
from src.cruds.videos_cruds import VideosCRUDS


class BaseParser:
    def __init__(self):
        self.__url_cruds = UrlsCRUDS()
        self.__videos_cruds = VideosCRUDS()

    def get_photo_and_videos_if_exists(self, base_info: dict, alibaba_id: UUID = None, amazon_id: UUID = None):
        keys = ("images", "videos")

        for key in keys:
            data = base_info.get(key)
            if data:
                for d in data:

                    if key == 'images':
                        print(d.get('link'))
                        print(key)
                        self.__url_cruds.insert_many_images(link=d.get('link'), amazon_id=amazon_id,
                                                            alibaba_id=alibaba_id)
                    elif key == 'videos':
                        self.__videos_cruds.insert_many_videos(link=d.get('link'), amazon_id=amazon_id,
                                                               alibaba_id=alibaba_id)
