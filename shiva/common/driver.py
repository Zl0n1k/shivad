from abc import ABC, abstractmethod
import asyncio
from collections import defaultdict

from loguru import logger
from shiva.const import MODULES_DRIVERS


class BaseDriver(ABC):
    def __init__(self, config, shiva):
        self.config = config
        self.shiva = shiva

    @abstractmethod
    async def prepare(self):
        raise NotImplementedError

    @abstractmethod
    async def stop(self, message):
        raise NotImplementedError


class Connections:
    def __init__(self, shiva, config):
        self.shiva = shiva
        self.config = config
        self.drivers_all = {}
        self.connections = {}

    @staticmethod
    async def connection_prepare(task_connections):
        # task_connection_prepare = [task_connection.prepare() for task_connection in task_connections]
        task_connection_prepare = [asyncio.create_task(task_connection.prepare()) for task_connection in task_connections] # ESB-2359
        done, _ = await asyncio.wait(task_connection_prepare, return_when=asyncio.ALL_COMPLETED)
        for result in done:
            result.result()

    async def prepare(self):
        for d in self.shiva.scopes[MODULES_DRIVERS].filter_members(BaseDriver):
            self.drivers_all[d.name] = d
        set_connection_level = set()
        task_connections_level = defaultdict(list)
        for k, v in self.config.get('connections', {}).items():
            if v['driver'] in self.drivers_all:
                connection_level = v.get('level') or 0
                connection = self.drivers_all[v['driver']](v['config'], self.shiva)
                connection.connection_name = k
                set_connection_level.add(connection_level)
                task_connections_level[connection_level].append(connection)
                self.connections[k] = connection
            else:
                logger.error(f'Unable to load driver: {k}[{v["driver"]}]: Driver not found!')
        for connection_level in set_connection_level:
            logger.info(f"Running LEVEL={connection_level}")
            task_connections = task_connections_level[connection_level]
            for connection in task_connections:
                logger.warning(f'Adding driver (LEVEL={connection_level}): '
                               f'{connection.connection_name}[{connection.name}]...')
            await self.connection_prepare(task_connections)
