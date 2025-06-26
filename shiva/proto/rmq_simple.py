import orjson
from loguru import logger
from shiva.common.base import BaseProtocol


class JSON_UnroutedALL(BaseProtocol):
    name = 'JSON_UnroutedALL'

    async def prepare(self):
        self.routes = {}
        logger.info('Loading proto workers...')
        for w, inst in self.workers.items():
            if inst:
                self.routes[w] = inst[0]  # Workers list(we nead at least one)[<class>, ....]

    async def dispatch(self, msg):
        for w_name, w_obj in self.routes.items():
            logger.debug(f'[Sending msg to: {w_name}]')
            await w_obj.run(msg.body)
