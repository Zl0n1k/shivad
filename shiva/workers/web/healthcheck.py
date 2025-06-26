from fastapi import APIRouter
from loguru import logger
from shiva.common.base import BaseWorker
from shiva.dispatchers.web import Web
from shiva.main import app

router = APIRouter(prefix='')
shiva = None


class Healthcheck(BaseWorker):
    name = 'healthcheck'
    dispatcher = Web

    @router.get("/readiness")
    def read():
        # print('*' * 80)
        # print('*' * 80)
        # print('*' * 80)
        # print(app.shiva)
        status = {
            'status': 'ok'
            # 'running': app.daemon.running,
            # 'channels': len(app.daemon.channels),
        }
        logger.debug('Healthcheck ok')
        return status

    @router.get("/liveness")
    def live():
        status = {
            'status': 'ok'
            # 'running': app.daemon.running,
            # 'channels': len(app.daemon.channels),
        }
        # logger.error('Daemon test!')
        # raise Exception('Some error')
        logger.debug('Liveness ok')
        return status
