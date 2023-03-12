from uuid import UUID

from clients.alibaba.alibaba_client import AlibabaClient


class AlibabaService:
    @staticmethod
    def search_by_photo_service(amazon_product_id: UUID):
        alibaba_client = AlibabaClient()

        return alibaba_client.search_by_upload_photo(amazon_product_id)

    @staticmethod
    def search_by_title_service(title: str) -> None:
        alibaba_client = AlibabaClient()

        alibaba_client.search_by_title(title)


alibaba_service = AlibabaService()
