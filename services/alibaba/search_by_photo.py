from clients.alibaba.alibaba_client import AlibabaClient


class AlibabaService:
    @staticmethod
    def search_by_photo_service(images: dict):
        alibaba_client = AlibabaClient()
        alibaba_client.search_by_upload_photo(images)

    @staticmethod
    def search_by_title_service(title: str):
        alibaba_client = AlibabaClient()

        alibaba_client.search_by_title(title)


alibaba_service = AlibabaService()
