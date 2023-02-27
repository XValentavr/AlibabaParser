from clients.amazon.amazon_client import AmazonClient


class AmazonService:
    @staticmethod
    def search_by_url(url: str):
        amazon_client = AmazonClient()
        images = amazon_client.search_on_url(url)
        amazon_client.close_browser()
        return images


amazon_service = AmazonService()
