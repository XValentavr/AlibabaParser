from collections import OrderedDict

from src.clients.alibaba.alibaba_client import AlibabaClient


class AlibabaService:
    @staticmethod
    def search_by_photo_service(
        images: dict, stored_index: int = 0
    ) -> list[OrderedDict]:
        alibaba_client = AlibabaClient()

        return alibaba_client.search_by_upload_photo(images, stored_index)

    @staticmethod
    def search_by_title_service(title: str) -> None:
        alibaba_client = AlibabaClient()

        alibaba_client.search_by_title(title)


alibaba_service = AlibabaService()
