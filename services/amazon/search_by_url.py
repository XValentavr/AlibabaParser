from clients.amazon.amazon_client import AmazonClient


class AmazonService:
    @staticmethod
    def search_by_url(url: str):
        amazon_client = AmazonClient()
        amazon_client.search_on_url(url)


amazon_service = AmazonService()
