from uuid import UUID

from clients.amazon.amazon_rainforest_api import AmazonRainforestAPI
from parsers.amazon.parse_url_to_asin import ParseUrlToAsin


class AmazonRainforestAPIClient:
    @staticmethod
    def get_products(url: str) -> UUID:
        parse_url = ParseUrlToAsin(url)
        asin = parse_url.parse()

        if asin:
            amazon_rainforest_api = AmazonRainforestAPI(asin, domain=None)

            return amazon_rainforest_api.get_product_full_info()
        return None


rainforest_api = AmazonRainforestAPIClient()
