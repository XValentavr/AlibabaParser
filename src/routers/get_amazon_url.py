from flask import Blueprint, request, jsonify

from ai.data_handlers.data_handler import DataHandler
from helpers.enums.alibaba.search_types import SearchTypes
from services.alibaba.search_by_photo import alibaba_service
from services.amazon.search_by_rainforest import rainforest_api
from services.amazon.search_by_url import amazon_service

amazon_link = Blueprint('amazon_link', __name__)


@amazon_link.route('/amazon', methods=["GET"])
def get_alibaba_links_from_amazon():
    search_type = request.args.get('type')
    photo = request.args.get('url')

    if search_type == SearchTypes.API:
        # rainforest api
        amazon_product_id = rainforest_api.get_products(photo)

        # get alibaba photos
        alibaba_product_ids = alibaba_service.search_by_photo_service(amazon_product_id)
        #  create aws handler
        data_handler = DataHandler(amazon_product_id, alibaba_product_ids)

        data_handler.aws_similarity()

    elif search_type == SearchTypes.SELENIUM:
        # selenium parser
        amazon_product_id = amazon_service.search_by_url(photo)

        alibaba_service.search_by_photo_service(amazon_product_id)
    else:
        return jsonify('No method found')
