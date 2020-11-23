from unittest.mock import patch
from models import redis_cli, Url
from faker import Faker
fake = Faker()


def test_get_origin_url(client):
    u = Url(origin_url=fake.uri(), short_url='fake_url')
    redis_cli.set(u.redis_key, u.json())

    resp = client.get(f'/v1/url/{u.short_url}')

    assert resp.status_code == 200
    assert resp.json.get('origin_url') == u.origin_url


def test_get_not_register_url(client):
    resp = client.get(f'/v1/url/zyxwv')

    assert resp.status_code == 400
    assert resp.json.get('message') is not None


def test_create_short_url(client):
    data = {'origin_url': fake.uri()}

    resp = client.post(f'/v1/url', data=data)

    assert resp.status_code == 200
    assert len(resp.json.get('short_url')) == Url.SHORT_URL_LENGTH


def test_create_no_origin_url(client):
    resp = client.post(f'/v1/url')

    assert resp.status_code == 400
    assert resp.json.get('message') is not None


def test_create_with_invalid_url(client):
    data = {'origin_url': 'abcdefghijklmnopqrstuvwxyz'}

    resp = client.post(f'/v1/url', data=data)

    assert resp.status_code == 400
    assert resp.json.get('message') is not None


def test_create_collision(client):
    data = {'origin_url': fake.uri()}

    with patch('models.redis_cli.set', return_value=False):
        resp = client.post(f'/v1/url', data=data)

    assert resp.status_code == 400
    assert resp.json.get('message') is not None


def test_get_urls_list(client):
    u = Url(origin_url=fake.uri(), short_url='fake_url')
    u2 = Url(origin_url=fake.uri(), short_url='fake_url_2')
    redis_cli.set(u.redis_key, u.json())
    redis_cli.set(u2.redis_key, u2.json())

    resp = client.get(f'/v1/url')

    assert resp.status_code == 200
    assert u in resp.json.get('urls')
    assert u2 in resp.json.get('urls')
