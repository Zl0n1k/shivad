import asyncio
from collections import defaultdict

from loguru import logger
from shiva.common.base import BaseDispatcher
from shiva.common.config import ConfigHelper
from shiva.const import MODULES_DISPATCHERS, MODULES_WORKERS


class DispatchersRoot:
    def __init__(self, shiva, config):
        self.shiva = shiva
        self.config = config
        self.dispatchers_all = {}
        self.dispatchers = defaultdict(dict)
        self.configurations = {}
        self.coro = []
        self.ch = ConfigHelper(self.config)
        self.disabled_list = {}
        self.configure()

    def configure(self):
        for d_name, cfg in self.ch.get_childs(MODULES_DISPATCHERS, {'enabled': True}):
            self.configurations[d_name] = cfg
            # logger.error(f'Dispatcher {d_name}')
        logger.info('Dispatchers configuration loaded!')

    async def prepare(self):
        # If we have non default dispatchers - ignore default one
        non_default = []
        # Collect all dispatchers
        for d in self.shiva.scopes[MODULES_DISPATCHERS].filter_members(BaseDispatcher):
            self.dispatchers_all[d.name] = d
        # Config first
        for inst_name, cfg in self.configurations.items():
            if cfg['dispatcher'] in self.dispatchers_all:
                non_default.append(cfg['dispatcher'])
                self.dispatchers[cfg['dispatcher']][inst_name] = self.dispatchers_all[cfg['dispatcher']](self.shiva, self.config, cfg)
                logger.info(f'Loading dispatcher: {cfg["dispatcher"]}[{inst_name}]({self.dispatchers_all[cfg["dispatcher"]]})')
        logger.info('Dispatchers loaded.')
        logger.info('Loading workers...')
        for d_name, d_data in self.dispatchers.items():
            for d_sub_name, d_obj in d_data.items():
                await d_obj.load(self.shiva.scopes[MODULES_WORKERS])
                await d_obj.prepare()
                # Prepare workers:
                for w_name, w_list in d_obj.workers.items():
                    for w in w_list:
                        if hasattr(w, 'prepare'):
                            await w.prepare()
        self.get_map()

    def get_map(self):
        for name, d in self.dispatchers.items():
            print(f'Dispatcher: {name}:')
            for d_name, d_obj in d.items():
                print(f'\tName: {d_name}')
                print(f'\tPolicy: {d_obj.dispatcher_config["policy"]}')
                print('\t\tWorkers:')
                for w_name, w_obj in d_obj.workers.items():
                    print(f'\t\t\t - {w_name}')
                    print(f'\t\t\t     coro: {len(w_obj)}')

    async def start(self):
        for d_name, d_inst in self.dispatchers.items():
            logger.info(f'Starting [{d_name}] instances...')
            for d_inst_name, d_obj in d_inst.items():
                logger.info(f'Starting [{d_inst_name}]...')
                await d_obj.start()
                self.coro += d_obj.coro
        # for name, dispatcher in self.dispatchers_all.items():
        #     logger.info(f'Starting {name}')
        #     self.coro.append(dispatcher.start())
