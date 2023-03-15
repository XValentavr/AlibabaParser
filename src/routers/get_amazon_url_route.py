from typing import Tuple

from flask import Blueprint, jsonify, request, Response

from clients.database.database_client import database_client
from exceptions.api_exception import APIException
from handlers.endpoint_handlers.amazon_endpoint_handler import amazon_endpoint_handler

amazon_link = Blueprint("amazon_link", __name__)


@amazon_link.route("/amazon", methods=["GET"])
def get_alibaba_links_from_amazon() -> Tuple[Response, int]:
    search_type = request.args.get('searchType')
    photo = request.args.get('amazonUrl')
    if not photo or not search_type:
        raise APIException(
            "get_alibaba_links_from_amazon",
            "No url of search type",
            403,
        )

    jsonify_response = amazon_endpoint_handler.parse_data(search_type=search_type, photo=photo)
    if not jsonify_response:
        return jsonify(database_client.send_most_similar_products()), 200

    return jsonify_response
