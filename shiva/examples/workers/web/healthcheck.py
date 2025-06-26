from fastapi import APIRouter
from loguru import logger

from shiva.common.base import BaseWorker
from shiva.dispatchers.web import Web

router = APIRouter(prefix='')
shiva = None


class Healthcheck(BaseWorker):
    name = 'healthcheck'
    dispatcher = Web

    @router.get("/readiness")
    def read():
        status = {
            'status': 'ok'
            # 'running': app.daemon.running,
            # 'channels': len(app.daemon.channels),
        }
        return status

    @router.get("/liveness")
    def live():
        status = {
            'status': 'ok'
            # 'running': app.daemon.running,
            # 'channels': len(app.daemon.channels),
        }
        logger.error('Daemon test!')
        # raise Exception('Some error')
        return status
