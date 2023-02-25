from clients.alibaba.alibaba_client import AlibabaClient


def search_by_photo_service(photo: str):
    alibaba_client = AlibabaClient()

    alibaba_client.search_by_upload_photo(photo)
