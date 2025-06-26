# Copyright (c) 2024 Boris Soldatov
# SPDX-License-Identifier: MIT
#
# This file is part of an open source project licensed under the MIT License.
# See the LICENSE file in the project root for more information.

from abc import ABC, abstractmethod
from collections import defaultdict

from loguru import logger

from shiva.common.config import ConfigHelper
from shiva.const import MODULES_WORKERS


class BaseDispatcher:
    base_class = None
    name = None
    load_workers = True

    def __init__(self, shiva, config, dispatcher_config={}):
        self.shiva = shiva
        self.config = config
        self.dispatcher_config = {'enabled': True, 'coro': 1, 'name': self.name, 'policy': 'ALL'}
        self.dispatcher_config.update(dispatcher_config)
        self.name = self.dispatcher_config['name']
        self.workers = defaultdict(list)
        self.coro = []
        self.workers_configurations = {}
        self.workers_all = {}
        self.workers = defaultdict(list)
        self.ch = ConfigHelper(self.config)
        self.policy_map = {
            'ALL': self.policy_all,
            'CONFIG': self.policy_config,
            'GROUP': None
        }
        self.policy = self.policy_map[self.dispatcher_config['policy']]

    async def prepare(self):
        pass

    async def load(self, scope):
        self.workers_scope = scope
        if self.load_workers:
            logger.info(f'[{self.dispatcher_config["name"]}]Preparing workers...')
            w_cls = scope.filter_members(self.base_class)
            for w in w_cls:
                # print(f'*********Trying to load [{w.name}] worker')
                w_dispatcher = None
                if hasattr(w, 'dispatcher'):
                    w_dispatcher = w.dispatcher
                # print(f'*********[{w.name}] dispatcher {w_dispatcher}: Current dispatcher: {self.dispatcher_config["name"]}')
                if w.name in self.workers_all:
                    logger.error(f'Worker already loaded: {w.name}. Check conflicting names.')
                if w_dispatcher and w_dispatcher == self.dispatcher_config['name']:
                    self.workers_all[w.name] = w
                    logger.info(f'Worker loaded: {w.name}')
                elif not w_dispatcher:
                    self.workers_all[w.name] = w
                    logger.info(f'Worker loaded: {w.name}')

            for w_name, cfg in self.ch.get_childs(MODULES_WORKERS, {'enabled': True}):
                if cfg.get('worker') in self.workers_all:
                    self.workers_configurations[w_name] = cfg
            logger.info(f'[{self.dispatcher_config["name"]}] Workers configuration loaded!')
            logger.info(f'[{self.dispatcher_config["name"]}]Loading workers(POLICY: {self.dispatcher_config["policy"]})...')
            self.policy()

    def policy_all(self):
        # Config first
        for w_sub_name, w_cfg in self.workers_configurations.items():
            dispatcher = self.is_compatible(w_cfg)
            if dispatcher:
                logger.warning(f'Loading {w_sub_name} to {dispatcher}')
                for w in range(w_cfg['coro']):
                    # self.workers[w_cfg['worker']].append(self.workers_all[w_cfg['worker']](self.shiva, self.config, w_cfg))
                    self.workers[w_cfg['name']].append(self.workers_all[w_cfg['worker']](self.shiva, self.config, w_cfg))
        # Other(not added from config)
        for w_name, w_cls in self.workers_all.items():
            if w_name not in self.workers:
                logger.warning(f'Loading {w_name} -> {self.name}')
                self.workers[w_name].append(w_cls(self.shiva, self.config))

    def policy_config(self):
        # Config first
        for w_sub_name, w_cfg in self.workers_configurations.items():
            dispatcher = self.is_compatible(w_cfg)
            if dispatcher:
                logger.warning(f'Loading {w_sub_name} to {dispatcher}')
                for w in range(w_cfg['coro']):
                    # self.workers[w_cfg['worker']].append(self.workers_all[w_cfg['worker']](self.shiva, self.config, w_cfg))
                    self.workers[w_cfg['name']].append(self.workers_all[w_cfg['worker']](self.shiva, self.config, w_cfg))

    def is_compatible(self, w_cfg):
        dispatcher = self.name
        logger.info(f'DISPATCHER DEFAULT: {dispatcher}')
        if hasattr(self.workers_all[w_cfg['worker']], 'dispatcher'):
            dispatcher = self.workers_all[w_cfg['worker']].dispatcher
        else:
            if w_cfg.get('dispatcher'):
                dispatcher = w_cfg['dispatcher']
        if dispatcher == self.dispatcher_config["name"]:
            return dispatcher

    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        raise NotImplementedError


class BaseWorker:
    def __init__(self, shiva, config, daemon_cfg=None):
        self.shiva = shiva
        self.config = config
        self.cfg_worker = daemon_cfg or {'enabled': True, 'coro': 1}

    async def prepare(self):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass


class BaseMetric:
    def __init__(self, shiva, config, cfg_worker={}):
        self.shiva = shiva
        self.config = config
        self.running = False
        self.coro = []
        self.cfg_worker = cfg_worker or {'enabled': True, 'coro': 1, 'name': self.name}
        self.cfg_worker.update(cfg_worker)
        if cfg_worker.get('name'):
            self.name = self.cfg_worker['name']
        # print(self.cfg_worker)

    @abstractmethod
    async def prepare(self):
        pass

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass


class BaseDaemon:
    def __init__(self, shiva, config, cfg_worker={}):
        self.shiva = shiva
        self.config = config
        self.running = False
        self.coro = []
        self.cfg_worker = cfg_worker or {'enabled': True, 'coro': 1, 'name': self.name}
        self.cfg_worker.update(cfg_worker)
        if cfg_worker.get('name'):
            self.name = self.cfg_worker['name']
        # print(self.cfg_worker)

    @abstractmethod
    async def prepare(self):
        pass

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass


class BaseRmqWorker:
    load_globals = ('router', )

    def __init__(self, shiva, config, daemon_cfg=None):
        self.shiva = shiva
        self.config = config
        self.cfg_worker = daemon_cfg or {'enabled': True, 'coro': 1}

    async def prepare(self):
        pass

    async def run(self):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass


class BaseProtocol:
    def __init__(self, shiva, workers):
        self.shiva = shiva
        self.workers = workers

    @abstractmethod
    async def prepare(self):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass

    async def run(self, msg):
        pass
