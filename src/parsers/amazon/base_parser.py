from uuid import UUID

from cruds.urls_cruds import UrlsCRUDS
from cruds.videos_cruds import VideosCRUDS


class BaseParser:
    """
    Class to extract image or video from amazon API response
    """

    def __init__(self):
        self.__url_cruds = UrlsCRUDS()
        self.__videos_cruds = VideosCRUDS()

    def get_photo_and_videos_if_exists(
        self, base_info: dict, alibaba_id: UUID = None, amazon_id: UUID = None
    ):
        """
        Get image or video from amazon API response if exists
        :param base_info: base response
        :param alibaba_id: alibaba product UUID to work with
        :param amazon_id: current amazon product ID
        :return:
        """
        keys = ("images", "videos")

        for key in keys:
            data = base_info.get(key)
            if data:
                for d in data:
                    if key == "images":
                        self.__url_cruds.insert_many_images(
                            link=d.get("link"),
                            amazon_id=amazon_id,
                            alibaba_id=alibaba_id,
                        )
                    elif key == "videos":
                        self.__videos_cruds.insert_many_videos(
                            link=d.get("link"),
                            amazon_id=amazon_id,
                            alibaba_id=alibaba_id,
                        )
