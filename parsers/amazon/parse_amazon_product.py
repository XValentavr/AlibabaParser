from collections import OrderedDict

from parsers.amazon.base_parser import BaseParser


class ParseAmazonProduct(BaseParser):
    def __init__(self, response):
        # maybe we need it
        self.__full_product = response

        self.__product_base_info = response.get("product")
        self.__dict = OrderedDict()

    def parse_full_data(self):
        return self.__get_product_all_info()

    def __get_product_all_info(self):
        title = self.__product_base_info.get("title")
        link = self.__product_base_info.get("link")

        # get all need data

        self.__dict.update({"title": title, "link": link})

        self.__dict.update(
            self.get_photo_and_videos_if_exists(self.__product_base_info)
        )

        self.__get_buybox()

        self.__get_description()

        return self.__dict

    def __get_buybox(self):
        product = self.__product_base_info.get("buybox_winner")
        price = product.get("price")

        self.__dict.update({"price": f"{price.get('value')}{price.get('symbol')}"})
        rrp_price = product.get("rrp")

        self.__dict.update(
            {"rrp_price": f"{rrp_price.get('value')}{rrp_price.get('symbol')}"}
        )

    def __get_description(self):
        description = self.__product_base_info.get("description")
        self.__dict.update({"description": description})
