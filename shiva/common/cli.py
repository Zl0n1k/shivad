import asyncio
import os

import yaml
from loguru import logger

from shiva.common.driver import Connections
from shiva.common.modules_helper import Scope
from shiva.const import CLI_SCOPES, SHIVA_ROOT
from shiva.lib.tools import Config


class ShivaCLI:
    def __init__(self):
        self.config = self.get_config()
        self.scopes = {}
        self.connections = None
        self.croot = None

    @staticmethod
    def get_config():
        config_path = os.environ.get("SHIVA_CONFIG") or "./config.yml"
        config_helper = Config(config_path)
        config = config_helper.get_config()
        return config
        # with open(cfg, encoding="utf8") as f:
        #     # config = flatdict.FlatDict(yaml.load(f, Loader=yaml.SafeLoader))
        #     config = yaml.load(f, Loader=yaml.SafeLoader)
        #     return config

    async def prepare(self):
        logger.info("Preparing...")
        self.load_scopes(CLI_SCOPES)
        await self.prepare_connections()

    async def prepare_connections(self):
        logger.info("Loading drivers...")
        self.croot = Connections(self, self.config)
        logger.info("Preparing drivers...")
        await self.croot.prepare()
        self.connections = self.croot.connections

    def load_scopes(self, scopes):
        logger.info("Loading shiva + user scopes...")

        for scope in scopes:
            sc_list = (f"{SHIVA_ROOT}.{scope}", scope)
            logger.info(f"Loading scopes: {sc_list}")
            self.scopes[scope] = Scope(scope, sc_list)
        for name, scope in self.scopes.items():
            logger.info(f"{name}: {len(scope.scopes)}")

    async def run(self):
        await self.prepare()
        await self.task()
        await self.stop_async()

    @staticmethod
    async def stop_async():
        import asyncio

        current_task = asyncio.current_task()
        tasks = [task for task in asyncio.all_tasks() if task is not current_task]
        for task in tasks:
            task.cancel()

    async def task(self):
        raise NotImplementedError
