
from fastapi import APIRouter
from fastapi_restful.inferring_router import InferringRouter
from loguru import logger

from shiva.common.base import BaseDispatcher, BaseWorker
from shiva.common.modules_helper import get_class_that_defined_method

# Black magic


class Web(BaseDispatcher):
    name = 'dispatcher_web'
    base_class = BaseWorker
    load_workers = False

    async def prepare(self):
        self.routers = []
        for s in self.workers_scope.scopes:
            if hasattr(s, 'router') and isinstance(s.router, (APIRouter, InferringRouter)):
                self.routers.append(s.router)
                # self.shiva.app.include_router(s.router)
        w_cls = self.workers_scope.filter_members(self.base_class)
        for w in w_cls:
            logger.info(f'WEB application loaded: {w.name}')
            if hasattr(w, 'call_prepare') and getattr(w, 'call_prepare') == True:
                inst = w()
                await inst.prepare()
        for router in self.routers:
            # router.shiva = self.shiva
            for r in router.routes:
                _cls = get_class_that_defined_method(r.endpoint)
                self.workers[f'[{_cls.name}]: {r.path}'] = [1, ]  # Hack for DispatchersRoot->map

    async def start(self):
        for router in self.routers:
            self.shiva.app.include_router(router)
            for r in router.routes:
                path = getattr(r, "path")
                logger.info(f'Web application started: {path}')

    async def stop(self):
        logger.warning(f'Stopped {self.name}')
