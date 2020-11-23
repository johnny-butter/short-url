import pytest
from app import create_app
from models import redis_cli


@pytest.fixture(scope='module')
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

    redis_cli.flushdb()
