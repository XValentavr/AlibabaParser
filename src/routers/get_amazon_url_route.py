from flask import Blueprint, jsonify, request

from clients.database.database_client import database_client
from cruds.result_similarity_cruds import ResultSimilarityCRUDS
from exceptions.api_exception import APIException
from handlers.endpoint_handlers.amazon_endpoint_handler import amazon_endpoint_handler
from helpers.dtos.most_similar_dto import MostSimilarDTO
from helpers.enums.alibaba.search_types import SearchTypes

amazon_link = Blueprint("amazon_link", __name__)


@amazon_link.route("/amazon", methods=["GET"])
def get_alibaba_links_from_amazon():
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
        return jsonify(database_client.send_most_similar_products())

    return jsonify_response
