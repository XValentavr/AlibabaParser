from src.clients.amazon.amazon_client import AmazonClient


class AmazonService:
    @staticmethod
    def search_by_url(url: str) -> dict:
        amazon_client = AmazonClient()

        amazon_product_id = amazon_client.search_on_url(url)
        amazon_client.close_tab()

        return amazon_product_id


amazon_service = AmazonService()
