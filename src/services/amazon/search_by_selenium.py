from clients.amazon.selenium.amazon_client import AmazonClient


class AmazonSearchBySeleniumService:
    """
    Class to work with selenium to get amazon product data
    """

    @staticmethod
    def search_by_url(url: str) -> dict:
        """
        Get amazon product info using selenium
        :param url: url to work with
        :return: amazon product UUID
        """
        amazon_client = AmazonClient()

        amazon_product_id = amazon_client.search_on_url(url)

        return amazon_product_id


amazon_search_by_selenium_service = AmazonSearchBySeleniumService()
