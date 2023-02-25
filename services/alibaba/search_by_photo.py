from clients.alibaba.alibaba_client import AlibabaClient


class AlibabaService:
    @staticmethod
    def search_by_photo_service(photo: str):
        alibaba_client = AlibabaClient()

        alibaba_client.search_by_upload_photo(photo)
        alibaba_client.close_browser()

    @staticmethod
    def search_by_title_service(title: str):
        alibaba_client = AlibabaClient()

        alibaba_client.search_by_title(title)


alibaba_service = AlibabaService()
