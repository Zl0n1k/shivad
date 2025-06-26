import asyncpg
from loguru import logger
from marshmallow import Schema, ValidationError, fields
from shiva.common.driver import BaseDriver


class Config(Schema):
    dsn = fields.String(required=True)
    pool_min = fields.Integer(required=False)
    pool_max = fields.Integer(required=False)
    max_inactive_connection_lifetime = fields.Integer(required=False)
    max_queries = fields.Integer(required=False)


class Pg(BaseDriver):
    name = 'postgres'

    def validate(self):
        self.config = Config().load(self.config)

    async def prepare(self) -> asyncpg.pool.Pool:
        """
        Init connection pool
        :return:
        """
        self.validate()
        self.pool: asyncpg.pool.Pool = await asyncpg.create_pool(
            dsn=self.config['dsn'],
            min_size=self.config['pool_min'],
            max_size=self.config['pool_max'],
            max_inactive_connection_lifetime=self.config['max_inactive_connection_lifetime'])
        return self.pool

    async def stop(self):
        logger.warning
        await self.pool.close()


if __name__ == '__main__':
    cfg = {
        # 'dsn': 'postgresql://postgres:@127.0.0.1:5432/trcont',
        'pool_min': 1,
        'pool_max': 50,
        'max_inactive_connection_lifetime': 300,
        'max_queries': 20
    }
    pg = Pg('p1', cfg)
