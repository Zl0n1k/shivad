import pymongo
from loguru import logger
from marshmallow import Schema, ValidationError, fields
from motor.motor_asyncio import AsyncIOMotorClient
from shiva.common.driver import BaseDriver


class Config(Schema):
    dsn = fields.String(required=True)
    pool_min = fields.Integer(required=False, default=1)
    pool_max = fields.Integer(required=False, default=50)
    indexes = fields.Dict(required=False)


class MongoDb(BaseDriver):
    name = 'mongodb'

    def validate(self):
        self.config = Config().load(self.config)

    async def prepare(self):
        """
        Init connection pool
        :return:
        """
        self.validate()
        self.pool = AsyncIOMotorClient(self.config['dsn'])

        # Indexes
        if self.config.get('indexes'):
            logger.info('Creating MongoDb indexes...')
            await self.create_indexes(self.config['indexes'])

        return self.pool

    async def create_indexes(self, indexes):
        for db_name, index_root in indexes.items():
            logger.info(f'Creating indexes for db: {db_name}')
            for collection_name, indexes_all in index_root.items():
                logger.info(f'Creating indexes for collection: {db_name}->{collection_name}')
                db = getattr(self.pool, db_name)
                collection = getattr(db, collection_name)
                for index_name, index_cfg in indexes_all.items():
                    indx = []
                    logger.info(f'Creating index [{db_name}->{collection_name}] {index_name}: {index_cfg}')
                    for indx_field, direction in index_cfg.items():
                        indx.append((indx_field, getattr(pymongo, direction)))
                    _ = await collection.create_index(indx, name=index_name)

    async def stop(self):
        logger.warning('Shutting down mongodb pool...')
        await self.pool.close()


if __name__ == '__main__':
    cfg = {
        # 'dsn': 'postgresql://postgres:@127.0.0.1:5432/trcont',
        'pool_min': 1,
        'pool_max': 50,
        'max_inactive_connection_lifetime': 300,
        'max_queries': 20
    }
    pg = MongoDb('p1', cfg)
