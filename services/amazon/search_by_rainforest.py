from clients.amazon.AmazonRainForesApi import AmazonRainForestAPI
from parsers.amazon.parseUrlToAsin import ParseUrlTiAsin


class AmazonRainforestAPIClient:

    @staticmethod
    def get_products(url: str):
        parse_url = ParseUrlTiAsin(url)
        asin = parse_url.parse()
        if asin:
            amazon_rainforest_api = AmazonRainForestAPI(asin, domain=None)
            product_info = amazon_rainforest_api.get_product_full_info()
            return dict(product_info)
        return 'An error occured'
