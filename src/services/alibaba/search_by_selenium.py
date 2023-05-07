from uuid import UUID

from clients.alibaba.selenium.alibaba_client import AlibabaClient


class AlibabaSearchBySeleniumService:
    """
    Class that handle endpoint and alibaba api client
    """

    @staticmethod
    def search_by_photo_service(amazon_product_id: UUID):
        """
        Get alibaba product using selenium
        :param amazon_product_id: already checked amazon product UUID
        :return: list of alibaba product UUIDs
        """
        alibaba_client = AlibabaClient()

        return alibaba_client.search_by_upload_photo(amazon_product_id)


alibaba_search_by_selenium = AlibabaSearchBySeleniumService()
