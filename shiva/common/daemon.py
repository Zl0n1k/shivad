import asyncio
import sys
import time

from loguru import logger
from shiva.common.dispatcher import DispatchersRoot
from shiva.common.driver import Connections
from shiva.common.modules_helper import Scope
from shiva.const import SCOPES, SHIVA_ROOT


class Shiva:
    def __init__(self, config, loop, app):
        self.config = config
        self.loop = loop
        self.app = app
        self.running = False
        self.stopped = True
        self.scopes = {}
        self.dispatchers = None
        self.connections = None
        self.droot = None
        self.croot = None
        self.data_exch = {}

    async def prepare(self):
        logger.info('Preparing...')
        self.load_scopes(SCOPES)
        await self.prepare_connections()
        await self.prepare_dispatchers()

    async def prepare_connections(self):
        logger.info('Loading drivers...')
        self.croot = Connections(self, self.config)
        logger.info('Preparing drivers...')
        await self.croot.prepare()
        self.connections = self.croot.connections

    async def prepare_dispatchers(self):
        logger.info('Loading dispatchers...')
        self.droot = DispatchersRoot(self, self.config)
        logger.info('Preparing dispatchers...')
        await self.droot.prepare()

    def load_scopes(self, scopes):
        logger.info('Loading shiva + user scopes...')

        for scope in scopes:
            sc_list = (f'{SHIVA_ROOT}.{scope}', scope)
            logger.info(f'Loading scopes: {sc_list}')
            self.scopes[scope] = Scope(scope, sc_list)
        for name, scope in self.scopes.items():
            logger.info(f'{name}: {len(scope.scopes)}')

    async def wait_coro(self):
        logger.info('Coro waiter started!')
        await self.droot.start()
        if self.droot.coro:
            task = [asyncio.create_task(t) for t in self.droot.coro] # ESB-2359
            await asyncio.wait(task)
        # logger.warning('Root coro waiter stopped!')
        logger.error('Root coro waiter stopped!')
        self.running = False

    async def run(self):
        self.running = True
        logger.warning(f'Starting Shiva...[{self}]')

        self.loop.create_task(self.wait_coro())
        self.stopped = False
        while self.running:
            # logger.info('*' * 40)
            # logger.info(f'RUNNING: {self}')
            # logger.info('*' * 40)
            await asyncio.sleep(2)
        self.loop.create_task(self.stop_async())

    async def stop_async(self):
        logger.info('Stopping...')
        logger.info('Waiting for daemon...')
        # print(self.droot.dispatchers)
        for d_name, d in self.droot.dispatchers.items():
            logger.warning(f'Trying to stop: {d_name} instances...')
            for inst_name, inst_obj in d.items():
                logger.warning(f'Stopping: {d_name}->{inst_name}')
                await inst_obj.stop()
        current_task = asyncio.current_task()
        # print(current_task)
        # print('*' * 80)
        tasks = [task for task in asyncio.all_tasks() if task is not current_task]
        for task in tasks:
            # print(f'T: {task}')
            task.cancel()
            # print('>>CANCELED')
        # print('!!!!!!!GATHER!!!!!!')
        # await asyncio.gather(*tasks, return_exceptions=True)
        logger.info('Shiva stopped.')

    def stop(self):
        self.running = False
        logger.warning('Stop command received!')
        # while not self.stopped:
        #     logger.warning('Waiting for Shiva to stop...')
        #     time.sleep(1)
        # sys.exit(0)
