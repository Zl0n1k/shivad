import asyncio
import importlib
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

    def _validate_scope_packages(self, packages):
        """
        Validate that scope packages are installed.

        Args:
            packages: List of package names to validate

        Returns:
            List of valid package names
        """
        valid_packages = []
        for package in packages:
            try:
                importlib.import_module(package)
                valid_packages.append(package)
                logger.info(f'Scope package "{package}" found')
            except ImportError:
                logger.warning(f'Scope package "{package}" not found, skipping')
        return valid_packages

    def load_scopes(self, scopes):
        logger.info("Loading shiva + packages + user scopes...")

        # Get additional packages from config
        scope_packages = self.config.get('scopes', {}).get('packages', [])
        valid_packages = self._validate_scope_packages(scope_packages)

        for scope in scopes:
            # Build scope loading chain
            # Order: shiva -> packages -> user
            sc_list = []

            # 1. Built-in shiva modules
            sc_list.append(f"{SHIVA_ROOT}.{scope}")

            # 2. Modules from installed packages
            for package in valid_packages:
                sc_list.append(f"{package}.{scope}")

            # 3. User modules
            sc_list.append(scope)

            # TODO: Current implementation loads first found module and skips duplicates.
            # If user modules need to override package modules, reverse the order.
            # See: shiva/common/modules_helper.py:Scope.load()

            logger.info(f'Scope "{scope}" loading order:')
            for idx, path in enumerate(sc_list, 1):
                logger.info(f"  {idx}. {path}")

            self.scopes[scope] = Scope(scope, sc_list)

        for name, scope in self.scopes.items():
            logger.info(f"{name}: {len(scope.scopes)} modules loaded")

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
