import aioredis
from loguru import logger
from marshmallow import Schema, ValidationError, fields
from shiva.common.driver import BaseDriver


class Config(Schema):
    dsn = fields.String(required=True)
    minsize = fields.Integer(required=False)
    maxsize = fields.Integer(required=False)


class Redis(BaseDriver):
    name = 'redis'

    def validate(self):
        self.config = Config().load(self.config)

    async def prepare(self):
        """
        Init connection pool
        :return:
        """
        self.validate()
        dsn = self.config.pop('dsn')
        self.pool = await aioredis.create_pool(dsn, **self.config)
        return self.pool
        # dsn = self.config.pop('dsn')
        # max_connections = self.config.get('maxsize', 10)
        # connection_pool = aioredis.ConnectionPool.from_url(dsn, max_connections=max_connections)
        # self.pool = aioredis.Redis(connection_pool=connection_pool)
        # return self.pool

    async def stop(self):
        logger.warning
        await self.pool.close()
