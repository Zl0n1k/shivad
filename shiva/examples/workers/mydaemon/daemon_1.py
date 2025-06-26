import asyncio

from loguru import logger
from shiva.common.base import BaseDaemon


class MyDaemon(BaseDaemon):
    name = 'first_shiva_daemon'

    async def prepare(self):
        pass

    async def start(self):
        logger.info('Daemon started!!!!!!!!!!!')
        self.running = True
        while self.running:
            logger.info('Daemon run!')
            logger.info('Daemon Sleep...')
            await asyncio.sleep(5)
        logger.warning(f'Stopped: {self.name}')

    async def stop(self):
        self.running = False
