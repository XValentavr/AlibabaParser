from typing import Tuple

from flask import Blueprint, jsonify, request, Response

from clients.database.database_client import database_client
from exceptions.api_exception import APIException
from handlers.endpoint_handlers.amazon_endpoint_handler import amazon_endpoint_handler
from helpers.check_if_uuid import is_valid_uuid

amazon_link = Blueprint("amazon_link", __name__)


@amazon_link.route("/amazon", methods=["GET"])
def get_alibaba_links_from_amazon() -> Tuple[Response, int]:
    """
    Main endpoint to compare alibaba and amazon products
    :return: response code
    """

    search_type_alibaba = request.args.get("searchTypeAlibaba")
    search_type_amazon = request.args.get("searchTypeAmazon")
    photo = request.args.get("amazonUrl")

    if not photo or not search_type_alibaba or not search_type_amazon:
        raise APIException(
            "get_alibaba_links_from_amazon",
            "No url of search type",
            403,
        )

    amazon_product_id = amazon_endpoint_handler.parse_data(
        search_type_amazon=search_type_amazon,
        search_type_alibaba=search_type_alibaba,
        photo=photo,
    )
    if amazon_product_id and is_valid_uuid(amazon_product_id):
        return jsonify(database_client.send_most_similar_products(amazon_product_id)), 200

    raise APIException(
        "no amazon product found",
        "No url of search type",
        403,
    )
