import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str = 'debug'

    FLASK_ENV: str = 'development'
    FLASK_HOST: str = '127.0.0.1'
    FLASK_PORT: str = '5000'

    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    API_ENDPOINT: str = 'http://127.0.0.1:5000'


class TestSettings(Settings):
    FLASK_ENV: str = 'test'

    REDIS_HOST: str = 'redis'
    REDIS_DB: int = 3


def get_settings():
    if os.getenv('FLASK_ENV', '') == 'test':
        return TestSettings(_env_file='.env_test')

    return Settings(_env_file='.env')


settings = get_settings()


if __name__ == '__main__':
    print(settings.dict())
