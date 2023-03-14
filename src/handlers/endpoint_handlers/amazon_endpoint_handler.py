from typing import Tuple

from flask import jsonify
from requests import Response

from ai.data_handlers.data_handler import DataHandler
from helpers.enums.alibaba.search_types import SearchTypes
from services.alibaba.search_by_photo import alibaba_service
from services.amazon.search_by_rainforest import rainforest_api
from services.amazon.search_by_url import amazon_service


class AmazonEndpointHandler:

    @staticmethod
    def parse_data(search_type: str, photo: str) -> Tuple[Response, int]:

        if search_type == SearchTypes.API:
            # rainforest api
            amazon_product_id = rainforest_api.get_products(photo)
            if amazon_product_id:
                # get alibaba photos
                alibaba_product_ids = alibaba_service.search_by_photo_service(
                    amazon_product_id
                )
                #  create aws handler
                data_handler = DataHandler(amazon_product_id, alibaba_product_ids)

                data_handler.aws_similarity()
            else:
                return jsonify("An error occurred"), 400

        elif search_type == SearchTypes.SELENIUM:
            # selenium parser
            amazon_product_id = amazon_service.search_by_url(photo)

            alibaba_service.search_by_photo_service(amazon_product_id)
        else:
            return jsonify("No method found"), 404


amazon_endpoint_handler = AmazonEndpointHandler()
