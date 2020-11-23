from models import Url


def test_generate_short_url():
    short_url = Url.gen_short_url()

    assert len(short_url) == Url.SHORT_URL_LENGTH
