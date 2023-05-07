from typing import Tuple

from flask import Blueprint, jsonify, request, Response

from clients.database.database_client import database_client
from exceptions.api_exception import APIException
from helpers.enums.table_models_enum import TableModelsEnum

amazon_link = Blueprint("clear_table", __name__)


@amazon_link.route("/clear", methods=["GET"])
def clear_specific_table() -> Tuple[Response, int]:
    """
    endpoint to clear tables (alibaba product or amazon)
    :return:  response status
    """
    deleter = request.args.get("deleteTable")
    if not deleter:
        raise APIException(
            "clear_specific_table",
            "No deleter to clear table",
            403,
        )

    if deleter == TableModelsEnum.ALIBABA:
        database_client.clear_alibaba_table()
        return jsonify("Succeed"), 200

    elif deleter == TableModelsEnum.AMAZON:
        database_client.clear_amazon_table()
        return jsonify("Succeed"), 200

    return jsonify("An error occurred"), 403
