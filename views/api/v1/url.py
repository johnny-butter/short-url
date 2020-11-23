from flask import Blueprint, request, jsonify
from models import redis_cli, Url
from errors import ApiException
from pydantic import ValidationError


api_v1_url = Blueprint('api_v1_url', __name__)


@api_v1_url.route('/url')
def list_():
    """
    List registered urls
    """
    keys = [k for k in redis_cli.scan_iter(match='url*', count=1000)]

    if not keys:
        return jsonify({'urls': []})

    # TODO: Pagination
    PAGE_SIZE = 25
    url_list = [Url.parse_raw(v).dict() for v in redis_cli.mget(*keys[-PAGE_SIZE:])]

    return jsonify({'urls': url_list})


@api_v1_url.route('/url', methods=['POST'])
def create():
    """
    Register the url
    """
    origin_url = request.values.get('origin_url', None)

    if not origin_url:
        raise ApiException('"origin_url" is required')

    MAX_TRY = 5

    for cnt in range(MAX_TRY):
        try:
            u = Url(short_url=Url.gen_short_url(), origin_url=origin_url)
        except ValidationError as e:
            raise ApiException(str(e))

        if redis_cli.set(u.redis_key, u.json(), nx=True, ex=u.SHORT_URL_EXPIRE_SECONDS):
            break

        if cnt + 1 == MAX_TRY:
            raise ApiException('Collision happened. Please try again.')

    return jsonify({'short_url': u.short_url})


@api_v1_url.route('/url/<string:short_url>')
def retrieve(short_url):
    """
    Retrieve the origin url from the short url
    """
    v = redis_cli.get(f'url:{short_url}')

    if not v:
        raise ApiException('The url not register yet')

    u = Url.parse_raw(v)
    redis_cli.expire(u.redis_key, u.SHORT_URL_EXPIRE_SECONDS)

    return jsonify({'origin_url': u.origin_url})
