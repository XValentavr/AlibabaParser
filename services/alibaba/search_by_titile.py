from clients.alibaba.alibaba_client import AlibabaClient


def search_by_title_service(title: str):
    alibaba_client = AlibabaClient()

    alibaba_client.search_by_title(title)
