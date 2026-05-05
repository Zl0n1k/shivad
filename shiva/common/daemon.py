import asyncio
import importlib
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
        logger.info("Preparing...")
        self.load_scopes(SCOPES)
        await self.prepare_connections()
        await self.prepare_dispatchers()

    async def prepare_connections(self):
        logger.info("Loading drivers...")
        self.croot = Connections(self, self.config)
        logger.info("Preparing drivers...")
        await self.croot.prepare()
        self.connections = self.croot.connections

    async def prepare_dispatchers(self):
        logger.info("Loading dispatchers...")
        self.droot = DispatchersRoot(self, self.config)
        logger.info("Preparing dispatchers...")
        await self.droot.prepare()

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
        scope_packages = self.config.get("scopes", {}).get("packages", [])
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

    async def wait_coro(self):
        logger.info("Coro waiter started!")
        await self.droot.start()
        if self.droot.coro:
            task = [asyncio.create_task(t) for t in self.droot.coro]  # ESB-2359
            await asyncio.wait(task)
        # logger.warning('Root coro waiter stopped!')
        logger.error("Root coro waiter stopped!")
        self.running = False

    async def run(self):
        self.running = True
        logger.warning(f"Starting Shiva...[{self}]")

        self.loop.create_task(self.wait_coro())
        self.stopped = False
        while self.running:
            # logger.info('*' * 40)
            # logger.info(f'RUNNING: {self}')
            # logger.info('*' * 40)
            await asyncio.sleep(2)
        # self.loop.create_task(self.stop_async())
        await self.stop_async()
        logger.info("STOP_ASYNC DONE!")

    async def stop_async(self):
        logger.info("Stopping...")
        logger.info("Waiting for daemon...")
        for d_name, d in self.droot.dispatchers.items():
            logger.warning(f"Trying to stop: {d_name} instances...")
            for inst_name, inst_obj in d.items():
                logger.warning(f"Stopping: {d_name}->{inst_name}")
                await inst_obj.stop()
        current_task = asyncio.current_task()
        tasks = [task for task in asyncio.all_tasks() if task is not current_task]
        for task in tasks:
            cancel = True
            service_names = ["LifespanOn.main", "LifespanOn", "Server.serve", "Shiva.wait_coro"]
            coro_name = str(task._coro)
            for s in service_names:
                if coro_name.find(s) >= 0:
                    cancel = False
            if cancel:
                logger.info(f"CANCELING TASK: {str(task._coro)}")
                task.cancel()
            else:
                logger.info(f"PASSING TASK: {str(task._coro)}")
        logger.info("Shiva stopped.")

    def stop(self):
        self.running = False
        logger.warning("Stop command received!")
