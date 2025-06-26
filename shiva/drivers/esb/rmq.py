import asyncio

import aio_pika
from aio_pika.pool import Pool
from loguru import logger
from shiva.common.driver import BaseDriver


class RabbitMq(BaseDriver):
    name = 'rmq'

    async def prepare(self):
        self.loop = asyncio.get_running_loop()

    async def get_connection(self):
        return await aio_pika.connect_robust(self.config['dsn'])

    async def stop(self):
        pass
