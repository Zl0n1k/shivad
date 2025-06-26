import asyncio
import datetime

from loguru import logger
from shiva.common.base import BaseRmqWorker
from shiva.common.rmq_routing import Router

router = Router()


class RmqBench(BaseRmqWorker):
    name = 'shiva_benchmark'
    dispatcher = 'shiva_bench'

    async def prepare(self):
        pass

    async def start(self):
        pass
        # print('&' * 100)
        # print('&' * 100)
        # print(self.exchanges)
        # print('&' * 100)

    @router.route('shiva.bench')
    async def bench(self, message, raw=None):
        logger.info('Bench.')
        # await asyncio.sleep(3)
