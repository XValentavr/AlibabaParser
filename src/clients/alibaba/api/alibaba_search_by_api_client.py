import logging
from typing import List, Dict
from uuid import UUID

import requests

from cruds.alibaba_product_ids_cruds import AlibabaProductIdsCRUDS
from helpers.constants import ALIBABA_PRODUCTS_LIST_MAX_LEN
from helpers.enums.alibaba.search_types import SearchTypes
from helpers.init_logger import create_logger
from helpers.project_envs import ProjectEnvs
from parsers.alibaba.parse_alibaba_product import ParseAlibabaProduct


class AlibabaSearchByApiClient:
    """
    This class is needed in order to get a product with api by product id
    """

    def __init__(self, amazon_product_id: UUID):
        self.__amazon_product_id = amazon_product_id
        self.__logger = create_logger()
        self.__alibaba_product_ids_cruds = AlibabaProductIdsCRUDS()

    @staticmethod
    def __create_endpoint_url_for_getting_products_by_text(keyword: str):
        """
        Create endpoint to get products by entered text
        :param product_id: id to get data from api
        :return: url to send request
        """
        return f"{ProjectEnvs.ALIBABA_BASE_ENDPOINT}item_search/?key={ProjectEnvs.ALIBABA_BASE_API_KEY}&&q={keyword}&&lang=en&secret={ProjectEnvs.ALIBABA_BASE_API_SECRET}"

    @staticmethod
    def __create_endpoint_url_for_getting_products(product_id: str):
        """
        Create endpoint to get product info
        :param product_id: id to get data from api
        :return: url to send request
        """
        return f"{ProjectEnvs.ALIBABA_BASE_ENDPOINT}item_get/?key={ProjectEnvs.ALIBABA_BASE_API_KEY}&&num_iid={product_id}&&lang=en&secret={ProjectEnvs.ALIBABA_BASE_API_SECRET}"

    def __get_alibaba_product_ids(self, from_where: SearchTypes):
        """
        Get product ids from database by amazon product id
        :return: list of alibaba product ids to get info about
        """
        return self.__alibaba_product_ids_cruds.get_alibaba_products_ids_by_amazon_product_id(
            amazon_id=self.__amazon_product_id,
            from_where=from_where
        )

    def make_api_request(self, from_where: SearchTypes):
        """
        This main method need to request data from api
        :return: alibaba products ids to work with AWS
        """
        product_with_errors: List = []
        alibaba_ids = self.__get_alibaba_product_ids(from_where)
        for alibaba in alibaba_ids:
            response = requests.get(self.__create_endpoint_url_for_getting_products(alibaba.product_id)).json()
            # response = self.test_data()
            self.__has_error(response, product_with_errors, alibaba)

        return [alibaba.alibaba_product_id for alibaba in alibaba_ids if
                alibaba.alibaba_product_id not in product_with_errors]

    def make_api_request_by_text(self, text: str):
        """
        Make request to api using celery task to get products by text
        """
        print('r', text)
        if text:
            response_products = requests.get(
                self.__create_endpoint_url_for_getting_products_by_text(keyword=text)).json()
            print('response_products', response_products)
            extracted_items = self.__extract_product_items(products=response_products)
            if extracted_items:
                self.__insert_alibaba_product_got_from_text_search(extracted_items,
                                                                   amazon_product_id=self.__amazon_product_id, )
                return self.make_api_request(from_where=SearchTypes.TEXT)  # type:ignore

    def __has_error(self, response, product_with_errors: list, alibaba):
        """
        Check if response from api contains error
        """
        if response.get('item') is not None:

            parse_alibaba_product = ParseAlibabaProduct(response)
            parse_alibaba_product.parse_full_data(alibaba.alibaba_product_id)
        else:
            self.__logger.setLevel(logging.DEBUG)
            self.__logger.error(response.get('error'))
            # raise Exception
            product_with_errors.append(alibaba.alibaba_product_id)

    @staticmethod
    def __extract_product_items(products: Dict):
        """
        Extract data from text search api result
        """
        if not products.get('error'):
            return products.get('items').get('item')

        return None

    @staticmethod
    def __insert_alibaba_product_got_from_text_search(alibaba_products: list, amazon_product_id: UUID):
        """
        insert data to table based on alibaba api response after text search
        """
        from clients.alibaba.api.alibaba_client_helper import alibaba_client_helper

        if len(alibaba_products) > ALIBABA_PRODUCTS_LIST_MAX_LEN:
            alibaba_products = alibaba_products[0:ALIBABA_PRODUCTS_LIST_MAX_LEN + 1]

        alibaba_client_helper.insert_alibaba_products(goods=alibaba_products,
                                                      amazon_product_id=amazon_product_id,
                                                      from_where=SearchTypes.TEXT)

    @staticmethod
    def test_data():
        return {
            "item": {
                "num_iid": "60840463360",
                "title": "Slip-on Daily Urban Walking Shoes ",
                "desc_short": "",
                "price": "$47.70",
                "nick": "cn1522808546pkux",
                "num": 9999,
                "min_num": 2,
                "detail_url": "https://www.alibaba.com/product-detail/Reebaby-Hot-Sell-Group-0-with_60840463360.html",
                "pic_url": "https://sc04.alicdn.com/kf/HTB1GHVXaPvuK1Rjy0Faq6x2aVXa7.jpg",
                "desc": '\r\n<p> <img src="//sc01.alicdn.com/kf/HTB1pHumyFmWBuNjSspdq6zugXXak/232931611/HTB1pHumyFmWBuNjSspdq6zugXXak.jpg" data-src="//sc01.alicdn.com/kf/HTB1pHumyFmWBuNjSspdq6zugXXak/232931611/HTB1pHumyFmWBuNjSspdq6zugXXak.jpg" data-alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="1117"></p>\n<noscript><img src="//sc01.alicdn.com/kf/HTB1pHumyFmWBuNjSspdq6zugXXak/232931611/HTB1pHumyFmWBuNjSspdq6zugXXak.jpg" alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="1117"></noscript>\n<img src="//sc01.alicdn.com/kf/HTB1jrTsyQ9WBuNjSspeq6yz5VXaR/232931611/HTB1jrTsyQ9WBuNjSspeq6yz5VXaR.jpg" data-src="//sc01.alicdn.com/kf/HTB1jrTsyQ9WBuNjSspeq6yz5VXaR/232931611/HTB1jrTsyQ9WBuNjSspeq6yz5VXaR.jpg" data-alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="890"><noscript><img src="//sc01.alicdn.com/kf/HTB1jrTsyQ9WBuNjSspeq6yz5VXaR/232931611/HTB1jrTsyQ9WBuNjSspeq6yz5VXaR.jpg" alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="890"></noscript>\n<img src="//sc01.alicdn.com/kf/HTB15.ciiHArBKNjSZFLq6A_dVXaA/232931611/HTB15.ciiHArBKNjSZFLq6A_dVXaA.jpg" data-src="//sc01.alicdn.com/kf/HTB15.ciiHArBKNjSZFLq6A_dVXaA/232931611/HTB15.ciiHArBKNjSZFLq6A_dVXaA.jpg" data-alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="1051"><noscript><img src="//sc01.alicdn.com/kf/HTB15.ciiHArBKNjSZFLq6A_dVXaA/232931611/HTB15.ciiHArBKNjSZFLq6A_dVXaA.jpg" alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="1051"></noscript>\n<img src="//sc01.alicdn.com/kf/HTB1qUMeyTlYBeNjSszcq6zwhFXao/232931611/HTB1qUMeyTlYBeNjSszcq6zwhFXao.jpg" data-src="//sc01.alicdn.com/kf/HTB1qUMeyTlYBeNjSszcq6zwhFXao/232931611/HTB1qUMeyTlYBeNjSszcq6zwhFXao.jpg" data-alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="656"><noscript><img src="//sc01.alicdn.com/kf/HTB1qUMeyTlYBeNjSszcq6zwhFXao/232931611/HTB1qUMeyTlYBeNjSszcq6zwhFXao.jpg" alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="656"></noscript>\n<img src="//sc01.alicdn.com/kf/HTB1TqSjiUOWBKNjSZKzq6xfWFXai/232931611/HTB1TqSjiUOWBKNjSZKzq6xfWFXai.jpg" data-src="//sc01.alicdn.com/kf/HTB1TqSjiUOWBKNjSZKzq6xfWFXai/232931611/HTB1TqSjiUOWBKNjSZKzq6xfWFXai.jpg" data-alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="1159"><noscript><img src="//sc01.alicdn.com/kf/HTB1TqSjiUOWBKNjSZKzq6xfWFXai/232931611/HTB1TqSjiUOWBKNjSZKzq6xfWFXai.jpg" alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="1159"></noscript>\n<img src="//sc01.alicdn.com/kf/HTB1qG0qiIIrBKNjSZK9q6ygoVXac/232931611/HTB1qG0qiIIrBKNjSZK9q6ygoVXac.jpg" data-src="//sc01.alicdn.com/kf/HTB1qG0qiIIrBKNjSZK9q6ygoVXac/232931611/HTB1qG0qiIIrBKNjSZK9q6ygoVXac.jpg" data-alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="1147"><noscript><img src="//sc01.alicdn.com/kf/HTB1qG0qiIIrBKNjSZK9q6ygoVXac/232931611/HTB1qG0qiIIrBKNjSZK9q6ygoVXac.jpg" alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="1147"></noscript>\n<img src="//sc01.alicdn.com/kf/HTB1iB7VyGmWBuNjy1Xaq6xCbXXa0/232931611/HTB1iB7VyGmWBuNjy1Xaq6xCbXXa0.jpg" data-src="//sc01.alicdn.com/kf/HTB1iB7VyGmWBuNjy1Xaq6xCbXXa0/232931611/HTB1iB7VyGmWBuNjy1Xaq6xCbXXa0.jpg" data-alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="610"><noscript><img src="//sc01.alicdn.com/kf/HTB1iB7VyGmWBuNjy1Xaq6xCbXXa0/232931611/HTB1iB7VyGmWBuNjy1Xaq6xCbXXa0.jpg" alt="Slip-On Daily Urban Walking Shoes" ori-width="790" ori-height="610"></noscript>\r\n<img src="https://www.o0b.cn/i.php?t.png&rid=gw-2.641b2c6d594bd&p=3279065513&k=73018&t=1679502447" style="display:none" />',
                "item_imgs": [
                    {
                        "url": "https://sc04.alicdn.com/kf/HTB1GHVXaPvuK1Rjy0Faq6x2aVXa7.jpg"
                    },
                    {
                        "url": "https://sc04.alicdn.com/kf/HTB1S8U6avfsK1RjSszbq6AqBXXaz.jpg"
                    },
                    {
                        "url": "https://sc04.alicdn.com/kf/HTB1LQA6apzsK1Rjy1Xbq6xOaFXak.jpg"
                    },
                    {
                        "url": "https://sc04.alicdn.com/kf/HTB1p8o8as_vK1Rjy0Foq6xIxVXaJ.jpg"
                    },
                    {
                        "url": "https://sc04.alicdn.com/kf/HTB1ZEZYasrrK1Rjy1zeq6xalFXai.jpg"
                    },
                    {
                        "url": "https://sc04.alicdn.com/kf/HTB1unN9azLuK1Rjy0Fhq6xpdFXaw.jpg"
                    },
                    {
                        "url": "https://sc04.alicdn.com/kf/HTB1ZUZYasrrK1Rjy1zeq6xalFXax.jpg"
                    },
                    {
                        "url": "https://sc04.alicdn.com/kf/HTB1bqkTayHrK1Rjy0Flq6AsaFXae.jpg"
                    },
                    {
                        "url": "https://sc04.alicdn.com/kf/HTB1CnsUasfrK1Rjy1Xdq6yemFXag.jpg"
                    },
                    {
                        "url": "https://sc04.alicdn.com/kf/HTB1.BsOasvrK1Rjy0Feq6ATmVXaD.jpg"
                    },
                    {
                        "url": "https://sc04.alicdn.com/kf/HTB1HpIUaDHuK1RkSndVq6xVwpXal.jpg"
                    },
                ],
                "video_url": "https://vod-icbu.alicdn.com/tB9FoF3YV1bEOMabUBf/fZIVRRvvNNNgnrI7rOB%40%40sd.mp4?w=896&h=504&e=sd&t=212caaa516795024455434212ef66d&b=icbu_video&p=*_icbu_vod_publish&tr=mp4-264-sd&iss=false",
                "props_name": "191288010:3327837:Color:black;191288010:3328925:Color:Pink;191288010:3331185:Color:White;191288010:3483425:Color:Grey;191288010:3851110:Color:Purple;191288010:-1:Color:navy;191288010:-2:Color:olive;214524521:190000791:Shoe Size:35;214524521:190000105:Shoe Size:36;214524521:29542:Shoe Size:37;214524521:28388:Shoe Size:38;214524521:190000792:Shoe Size:39;214524521:28389:Shoe Size:40;214524521:28390:Shoe Size:41;214524521:28391:Shoe Size:42;214524521:28392:Shoe Size:43;214524521:28393:Shoe Size:44;214524521:28394:Shoe Size:45;214524521:28395:Shoe Size:46",
                "prop_imgs": {
                    "prop_img": [
                        {
                            "properties": "191288010:3327837",
                            "url": "https://sc04.alicdn.com/kf/HTB1ZEZYasrrK1Rjy1zeq6xalFXai.jpg",
                        },
                        {
                            "properties": "191288010:3328925",
                            "url": "https://sc04.alicdn.com/kf/HTB1unN9azLuK1Rjy0Fhq6xpdFXaw.jpg",
                        },
                        {
                            "properties": "191288010:3331185",
                            "url": "https://sc04.alicdn.com/kf/HTB1ZUZYasrrK1Rjy1zeq6xalFXax.jpg",
                        },
                        {
                            "properties": "191288010:3483425",
                            "url": "https://sc04.alicdn.com/kf/HTB1bqkTayHrK1Rjy0Flq6AsaFXae.jpg",
                        },
                        {
                            "properties": "191288010:3851110",
                            "url": "https://sc04.alicdn.com/kf/HTB1CnsUasfrK1Rjy1Xdq6yemFXag.jpg",
                        },
                        {
                            "properties": "191288010:-1",
                            "url": "https://sc04.alicdn.com/kf/HTB1.BsOasvrK1Rjy0Feq6ATmVXaD.jpg",
                        },
                        {
                            "properties": "191288010:-2",
                            "url": "https://sc04.alicdn.com/kf/HTB1HpIUaDHuK1RkSndVq6xVwpXal.jpg",
                        },
                    ]
                },
                "props": [
                    {"name": "Place of Origin", "value": "China"},
                    {"name": "Brand Name", "value": "HOTPOTATO"},
                    {"name": "Model Number", "value": "G2"},
                    {"name": "Midsole Material", "value": "EVA"},
                    {"name": "Outsole Material", "value": "Rubber"},
                    {"name": "Lining Material", "value": "Mesh"},
                    {"name": "Gender", "value": "Men"},
                    {"name": "gender", "value": "men"},
                    {"name": "Upper Material", "value": "fly knit nylon + TPU"},
                    {"name": "Material", "value": "fly knit"},
                    {"name": "Key words", "value": "Fashionable Light Shoes"},
                    {"name": "Type", "value": "Casual Ladies Flat Loafer  Shoes"},
                    {"name": "Feature", "value": "Light Weight"},
                    {"name": "MOQ", "value": "60 Pairs"},
                ],
                "skus": {
                    "sku": [
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:28393",
                            "properties_name": "191288010:-1:Color:navy;214524521:28393:Shoe Size:44",
                            "quantity": "999",
                            "sku_id": 274257648,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:28389",
                            "properties_name": "191288010:-1:Color:navy;214524521:28389:Shoe Size:40",
                            "quantity": "999",
                            "sku_id": 274257644,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:28388",
                            "properties_name": "191288010:3331185:Color:White;214524521:28388:Shoe Size:38",
                            "quantity": "999",
                            "sku_id": 11485006210,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:28395",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:28395:Shoe Size:46",
                            "quantity": "999",
                            "sku_id": 274257682,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:28390",
                            "properties_name": "191288010:3327837:Color:black;214524521:28390:Shoe Size:41",
                            "quantity": "999",
                            "sku_id": 274257637,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:28391",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:28391:Shoe Size:42",
                            "quantity": "999",
                            "sku_id": 268870709,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:29542",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:29542:Shoe Size:37",
                            "quantity": "999",
                            "sku_id": 11485006217,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:28391",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:28391:Shoe Size:42",
                            "quantity": "999",
                            "sku_id": 274257678,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:28394",
                            "properties_name": "191288010:3327837:Color:black;214524521:28394:Shoe Size:45",
                            "quantity": "999",
                            "sku_id": 274257641,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:28392",
                            "properties_name": "191288010:3331185:Color:White;214524521:28392:Shoe Size:43",
                            "quantity": "999",
                            "sku_id": 274257663,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:28393",
                            "properties_name": "191288010:-2:Color:olive;214524521:28393:Shoe Size:44",
                            "quantity": "999",
                            "sku_id": 274257656,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:190000792",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:190000792:Shoe Size:39",
                            "quantity": "999",
                            "sku_id": 274257675,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:29542",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:29542:Shoe Size:37",
                            "quantity": "999",
                            "sku_id": 11485006205,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:28395",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:28395:Shoe Size:46",
                            "quantity": "999",
                            "sku_id": 268870713,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:28395",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:28395:Shoe Size:46",
                            "quantity": "999",
                            "sku_id": 274257674,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:28389",
                            "properties_name": "191288010:-2:Color:olive;214524521:28389:Shoe Size:40",
                            "quantity": "999",
                            "sku_id": 274257652,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:28391",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:28391:Shoe Size:42",
                            "quantity": "999",
                            "sku_id": 274257670,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:28392",
                            "properties_name": "191288010:-1:Color:navy;214524521:28392:Shoe Size:43",
                            "quantity": "999",
                            "sku_id": 274257647,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:28394",
                            "properties_name": "191288010:-1:Color:navy;214524521:28394:Shoe Size:45",
                            "quantity": "999",
                            "sku_id": 274257649,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:29542",
                            "properties_name": "191288010:-2:Color:olive;214524521:29542:Shoe Size:37",
                            "quantity": "999",
                            "sku_id": 11485006229,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:28388",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:28388:Shoe Size:38",
                            "quantity": "999",
                            "sku_id": 11485006222,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:28388",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:28388:Shoe Size:38",
                            "quantity": "999",
                            "sku_id": 11485006206,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:28389",
                            "properties_name": "191288010:3331185:Color:White;214524521:28389:Shoe Size:40",
                            "quantity": "999",
                            "sku_id": 274257660,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:28391",
                            "properties_name": "191288010:3327837:Color:black;214524521:28391:Shoe Size:42",
                            "quantity": "999",
                            "sku_id": 274257638,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:29542",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:29542:Shoe Size:37",
                            "quantity": "999",
                            "sku_id": 11485006221,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:28393",
                            "properties_name": "191288010:3331185:Color:White;214524521:28393:Shoe Size:44",
                            "quantity": "999",
                            "sku_id": 274257664,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:28390",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:28390:Shoe Size:41",
                            "quantity": "999",
                            "sku_id": 268870708,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:28395",
                            "properties_name": "191288010:3327837:Color:black;214524521:28395:Shoe Size:46",
                            "quantity": "999",
                            "sku_id": 274257642,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:190000791",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:190000791:Shoe Size:35",
                            "quantity": "999",
                            "sku_id": 11485006219,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:28391",
                            "properties_name": "191288010:-2:Color:olive;214524521:28391:Shoe Size:42",
                            "quantity": "999",
                            "sku_id": 274257654,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:28392",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:28392:Shoe Size:43",
                            "quantity": "999",
                            "sku_id": 274257679,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:28392",
                            "properties_name": "191288010:-2:Color:olive;214524521:28392:Shoe Size:43",
                            "quantity": "999",
                            "sku_id": 274257655,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:28394",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:28394:Shoe Size:45",
                            "quantity": "999",
                            "sku_id": 268870712,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:29542",
                            "properties_name": "191288010:3331185:Color:White;214524521:29542:Shoe Size:37",
                            "quantity": "999",
                            "sku_id": 11485006209,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:28388",
                            "properties_name": "191288010:-2:Color:olive;214524521:28388:Shoe Size:38",
                            "quantity": "999",
                            "sku_id": 11485006230,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:190000791",
                            "properties_name": "191288010:-1:Color:navy;214524521:190000791:Shoe Size:35",
                            "quantity": "999",
                            "sku_id": 11485006223,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:190000105",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:190000105:Shoe Size:36",
                            "quantity": "999",
                            "sku_id": 11485006220,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:28392",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:28392:Shoe Size:43",
                            "quantity": "999",
                            "sku_id": 274257671,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:190000105",
                            "properties_name": "191288010:-1:Color:navy;214524521:190000105:Shoe Size:36",
                            "quantity": "999",
                            "sku_id": 11485006224,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:28395",
                            "properties_name": "191288010:-1:Color:navy;214524521:28395:Shoe Size:46",
                            "quantity": "999",
                            "sku_id": 274257650,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:190000792",
                            "properties_name": "191288010:3331185:Color:White;214524521:190000792:Shoe Size:39",
                            "quantity": "999",
                            "sku_id": 274257659,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:28389",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:28389:Shoe Size:40",
                            "quantity": "999",
                            "sku_id": 274257668,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:28389",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:28389:Shoe Size:40",
                            "quantity": "999",
                            "sku_id": 274257676,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:28393",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:28393:Shoe Size:44",
                            "quantity": "999",
                            "sku_id": 268870711,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:28394",
                            "properties_name": "191288010:3331185:Color:White;214524521:28394:Shoe Size:45",
                            "quantity": "999",
                            "sku_id": 274257665,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:28392",
                            "properties_name": "191288010:3327837:Color:black;214524521:28392:Shoe Size:43",
                            "quantity": "999",
                            "sku_id": 274257639,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:190000792",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:190000792:Shoe Size:39",
                            "quantity": "999",
                            "sku_id": 274257667,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:28393",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:28393:Shoe Size:44",
                            "quantity": "999",
                            "sku_id": 274257680,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:28390",
                            "properties_name": "191288010:-2:Color:olive;214524521:28390:Shoe Size:41",
                            "quantity": "999",
                            "sku_id": 274257653,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:190000105",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:190000105:Shoe Size:36",
                            "quantity": "999",
                            "sku_id": 11485006216,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:28390",
                            "properties_name": "191288010:3331185:Color:White;214524521:28390:Shoe Size:41",
                            "quantity": "999",
                            "sku_id": 274257661,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:28389",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:28389:Shoe Size:40",
                            "quantity": "999",
                            "sku_id": 268870707,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:28388",
                            "properties_name": "191288010:3327837:Color:black;214524521:28388:Shoe Size:38",
                            "quantity": "999",
                            "sku_id": 11485006214,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:29542",
                            "properties_name": "191288010:-1:Color:navy;214524521:29542:Shoe Size:37",
                            "quantity": "999",
                            "sku_id": 11485006225,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:28395",
                            "properties_name": "191288010:-2:Color:olive;214524521:28395:Shoe Size:46",
                            "quantity": "999",
                            "sku_id": 274257658,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:190000791",
                            "properties_name": "191288010:-2:Color:olive;214524521:190000791:Shoe Size:35",
                            "quantity": "999",
                            "sku_id": 11485006227,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:190000792",
                            "properties_name": "191288010:-1:Color:navy;214524521:190000792:Shoe Size:39",
                            "quantity": "999",
                            "sku_id": 274257643,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:190000792",
                            "properties_name": "191288010:3327837:Color:black;214524521:190000792:Shoe Size:39",
                            "quantity": "999",
                            "sku_id": 274257635,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:190000791",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:190000791:Shoe Size:35",
                            "quantity": "999",
                            "sku_id": 11485006215,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:190000105",
                            "properties_name": "191288010:-2:Color:olive;214524521:190000105:Shoe Size:36",
                            "quantity": "999",
                            "sku_id": 11485006228,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:28393",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:28393:Shoe Size:44",
                            "quantity": "999",
                            "sku_id": 274257672,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:28390",
                            "properties_name": "191288010:-1:Color:navy;214524521:28390:Shoe Size:41",
                            "quantity": "999",
                            "sku_id": 274257645,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:29542",
                            "properties_name": "191288010:3327837:Color:black;214524521:29542:Shoe Size:37",
                            "quantity": "999",
                            "sku_id": 11485006213,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:190000791",
                            "properties_name": "191288010:3331185:Color:White;214524521:190000791:Shoe Size:35",
                            "quantity": "999",
                            "sku_id": 11485006207,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:28388",
                            "properties_name": "191288010:-1:Color:navy;214524521:28388:Shoe Size:38",
                            "quantity": "999",
                            "sku_id": 11485006226,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:190000792",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:190000792:Shoe Size:39",
                            "quantity": "999",
                            "sku_id": 268870706,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:28395",
                            "properties_name": "191288010:3331185:Color:White;214524521:28395:Shoe Size:46",
                            "quantity": "999",
                            "sku_id": 274257666,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:28392",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:28392:Shoe Size:43",
                            "quantity": "999",
                            "sku_id": 268870710,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:28394",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:28394:Shoe Size:45",
                            "quantity": "999",
                            "sku_id": 274257681,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:28393",
                            "properties_name": "191288010:3327837:Color:black;214524521:28393:Shoe Size:44",
                            "quantity": "999",
                            "sku_id": 274257640,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:28391",
                            "properties_name": "191288010:3331185:Color:White;214524521:28391:Shoe Size:42",
                            "quantity": "999",
                            "sku_id": 274257662,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:28390",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:28390:Shoe Size:41",
                            "quantity": "999",
                            "sku_id": 274257677,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:190000105",
                            "properties_name": "191288010:3327837:Color:black;214524521:190000105:Shoe Size:36",
                            "quantity": "999",
                            "sku_id": 11485006212,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3331185;214524521:190000105",
                            "properties_name": "191288010:3331185:Color:White;214524521:190000105:Shoe Size:36",
                            "quantity": "999",
                            "sku_id": 11485006208,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:190000792",
                            "properties_name": "191288010:-2:Color:olive;214524521:190000792:Shoe Size:39",
                            "quantity": "999",
                            "sku_id": 274257651,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:190000791",
                            "properties_name": "191288010:3327837:Color:black;214524521:190000791:Shoe Size:35",
                            "quantity": "999",
                            "sku_id": 11485006211,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:190000791",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:190000791:Shoe Size:35",
                            "quantity": "999",
                            "sku_id": 11485006203,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:28390",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:28390:Shoe Size:41",
                            "quantity": "999",
                            "sku_id": 274257669,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3327837;214524521:28389",
                            "properties_name": "191288010:3327837:Color:black;214524521:28389:Shoe Size:40",
                            "quantity": "999",
                            "sku_id": 274257636,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-2;214524521:28394",
                            "properties_name": "191288010:-2:Color:olive;214524521:28394:Shoe Size:45",
                            "quantity": "999",
                            "sku_id": 274257657,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3483425;214524521:28388",
                            "properties_name": "191288010:3483425:Color:Grey;214524521:28388:Shoe Size:38",
                            "quantity": "999",
                            "sku_id": 11485006218,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:-1;214524521:28391",
                            "properties_name": "191288010:-1:Color:navy;214524521:28391:Shoe Size:42",
                            "quantity": "999",
                            "sku_id": 274257646,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3851110;214524521:190000105",
                            "properties_name": "191288010:3851110:Color:Purple;214524521:190000105:Shoe Size:36",
                            "quantity": "999",
                            "sku_id": 11485006204,
                        },
                        {
                            "price": 47.7,
                            "properties": "191288010:3328925;214524521:28394",
                            "properties_name": "191288010:3328925:Color:Pink;214524521:28394:Shoe Size:45",
                            "quantity": "999",
                            "sku_id": 274257673,
                        },
                    ]
                },
                "priceRange": [[2, 47.7], [1200, 17.9], [2700, 16.1], [6300, 15.6]],
                "props_list": {
                    "191288010:3327837": "Color:black",
                    "191288010:3328925": "Color:Pink",
                    "191288010:3331185": "Color:White",
                    "191288010:3483425": "Color:Grey",
                    "191288010:3851110": "Color:Purple",
                    "191288010:-1": "Color:navy",
                    "191288010:-2": "Color:olive",
                    "214524521:190000791": "Shoe Size:35",
                    "214524521:190000105": "Shoe Size:36",
                    "214524521:29542": "Shoe Size:37",
                    "214524521:28388": "Shoe Size:38",
                    "214524521:190000792": "Shoe Size:39",
                    "214524521:28389": "Shoe Size:40",
                    "214524521:28390": "Shoe Size:41",
                    "214524521:28391": "Shoe Size:42",
                    "214524521:28392": "Shoe Size:43",
                    "214524521:28393": "Shoe Size:44",
                    "214524521:28394": "Shoe Size:45",
                    "214524521:28395": "Shoe Size:46",
                },
                "seller_info": {
                    "zhuy": "",
                    "title": "",
                    "nick": "cn1522808546pkux",
                    "shop_name": "",
                },
                "error": "",
                "props_img": {
                    "191288010:3327837": "https://sc04.alicdn.com/kf/HTB1ZEZYasrrK1Rjy1zeq6xalFXai.jpg",
                    "191288010:3328925": "https://sc04.alicdn.com/kf/HTB1unN9azLuK1Rjy0Fhq6xpdFXaw.jpg",
                    "191288010:3331185": "https://sc04.alicdn.com/kf/HTB1ZUZYasrrK1Rjy1zeq6xalFXax.jpg",
                    "191288010:3483425": "https://sc04.alicdn.com/kf/HTB1bqkTayHrK1Rjy0Flq6AsaFXae.jpg",
                    "191288010:3851110": "https://sc04.alicdn.com/kf/HTB1CnsUasfrK1Rjy1Xdq6yemFXag.jpg",
                    "191288010:-1": "https://sc04.alicdn.com/kf/HTB1.BsOasvrK1Rjy0Feq6ATmVXaD.jpg",
                    "191288010:-2": "https://sc04.alicdn.com/kf/HTB1HpIUaDHuK1RkSndVq6xVwpXal.jpg",
                },
                "currency_code": "USD",
                "language_code": "en",
                "format_check": "ok",
                "sales": 0,
                "desc_img": [
                    "//sc01.alicdn.com/kf/HTB1pHumyFmWBuNjSspdq6zugXXak/232931611/HTB1pHumyFmWBuNjSspdq6zugXXak.jpg",
                    "//sc01.alicdn.com/kf/HTB1pHumyFmWBuNjSspdq6zugXXak/232931611/HTB1pHumyFmWBuNjSspdq6zugXXak.jpg",
                    "//sc01.alicdn.com/kf/HTB1jrTsyQ9WBuNjSspeq6yz5VXaR/232931611/HTB1jrTsyQ9WBuNjSspeq6yz5VXaR.jpg",
                    "//sc01.alicdn.com/kf/HTB1jrTsyQ9WBuNjSspeq6yz5VXaR/232931611/HTB1jrTsyQ9WBuNjSspeq6yz5VXaR.jpg",
                    "//sc01.alicdn.com/kf/HTB15.ciiHArBKNjSZFLq6A_dVXaA/232931611/HTB15.ciiHArBKNjSZFLq6A_dVXaA.jpg",
                    "//sc01.alicdn.com/kf/HTB15.ciiHArBKNjSZFLq6A_dVXaA/232931611/HTB15.ciiHArBKNjSZFLq6A_dVXaA.jpg",
                    "//sc01.alicdn.com/kf/HTB1qUMeyTlYBeNjSszcq6zwhFXao/232931611/HTB1qUMeyTlYBeNjSszcq6zwhFXao.jpg",
                    "//sc01.alicdn.com/kf/HTB1qUMeyTlYBeNjSszcq6zwhFXao/232931611/HTB1qUMeyTlYBeNjSszcq6zwhFXao.jpg",
                    "//sc01.alicdn.com/kf/HTB1TqSjiUOWBKNjSZKzq6xfWFXai/232931611/HTB1TqSjiUOWBKNjSZKzq6xfWFXai.jpg",
                    "//sc01.alicdn.com/kf/HTB1TqSjiUOWBKNjSZKzq6xfWFXai/232931611/HTB1TqSjiUOWBKNjSZKzq6xfWFXai.jpg",
                    "//sc01.alicdn.com/kf/HTB1qG0qiIIrBKNjSZK9q6ygoVXac/232931611/HTB1qG0qiIIrBKNjSZK9q6ygoVXac.jpg",
                    "//sc01.alicdn.com/kf/HTB1qG0qiIIrBKNjSZK9q6ygoVXac/232931611/HTB1qG0qiIIrBKNjSZK9q6ygoVXac.jpg",
                    "//sc01.alicdn.com/kf/HTB1iB7VyGmWBuNjy1Xaq6xCbXXa0/232931611/HTB1iB7VyGmWBuNjy1Xaq6xCbXXa0.jpg",
                    "//sc01.alicdn.com/kf/HTB1iB7VyGmWBuNjy1Xaq6xCbXXa0/232931611/HTB1iB7VyGmWBuNjy1Xaq6xCbXXa0.jpg",
                ],
                "shop_item": [],
                "relate_items": [],
            },
            "error": "",
            "secache": "7b6c51b57c7ea5395370ed27581e4f30",
            "secache_time": 1679502447,
            "secache_date": "2023-03-23 00:27:27",
            "translate_status": "",
            "translate_time": 0,
            "language": {"default_lang": "en", "current_lang": "en"},
            "reason": "",
            "error_code": "0000",
            "cache": 0,
            "api_info": "today:9 max:200 all[17=9+0+8];expires:2023-03-25",
            "execution_time": "1.869",
            "server_time": "Beijing/2023-03-23 00:27:27",
            "client_ip": "195.114.145.169",
            "call_args": {"num_iid": "60840463360"},
            "api_type": "alibaba",
            "translate_language": "en",
            "translate_engine": "baidu",
            "server_memory": "5.24MB",
            "request_id": "gw-2.641b2c6d594bd",
            "last_id": "1634503471",
        }
