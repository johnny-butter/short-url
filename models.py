import redis
import shortuuid
from pydantic import BaseModel, HttpUrl
from typing import ClassVar
from settings import settings


_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

redis_cli = redis.Redis(connection_pool=_pool)


class Model(BaseModel):

    @property
    def pk(self):
        if not hasattr(self, '_pk_filed_name'):
            raise ValueError('"_pk_filed_name" must be set')

        if not hasattr(self, self._pk_filed_name):
            raise ValueError(f'"{self._pk_filed_name}" not in the model')

        return getattr(self, self._pk_filed_name)

    @property
    def table_name(self):
        return self.__class__.__name__.lower()

    @property
    def redis_key(self):
        return f'{self.table_name}:{self.pk}'


class Url(Model):
    _pk_filed_name = 'short_url'

    short_url: str
    origin_url: HttpUrl

    SHORT_URL_LENGTH: ClassVar = 5
    SHORT_URL_EXPIRE_SECONDS: ClassVar = 60 * 5

    @classmethod
    def gen_short_url(cls):
        return shortuuid.ShortUUID().random(length=cls.SHORT_URL_LENGTH)
