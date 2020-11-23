from flask import Blueprint, jsonify
from errors import ApiException


error_handler = Blueprint('error_handler', __name__)


@error_handler.app_errorhandler(ApiException)
def handle_api_exception(err):
    resp = jsonify(err.to_dict())
    resp.status_code = err.status_code

    return resp


@error_handler.app_errorhandler(400)
@error_handler.app_errorhandler(500)
def handle_internal_error(err):
    origin_err = getattr(err, 'original_exception', None)
    err_msg = {'message': 'Internal Server Error'}
    if origin_err:
        err_msg = {'message': str(origin_err)}

    resp = jsonify(err_msg)
    resp.status_code = 500

    return resp
