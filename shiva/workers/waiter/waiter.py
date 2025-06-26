import asyncio

from loguru import logger
from shiva.common.base import BaseDaemon


class MyDaemon(BaseDaemon):
    name = 'waiter_daemon'

    async def prepare(self):
        pass

    async def start(self):
        logger.info('Waiter started!')
        self.running = True
        while self.running:
            # logger.info('Waiter sleep...')
            await asyncio.sleep(5)
        logger.warning(f'Stopped: {self.name}')

    async def stop(self):
        self.running = False
