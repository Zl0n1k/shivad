import asyncio
import logging

import uvloop
from loguru import logger
from shiva.main import daemon

# UVLOOP
# loop = asyncio.get_event_loop()
# asyncio.set_event_loop(loop)
# uvloop.install()

# logger = logging.getLogger("run")

# if __name__ == '__main__':
#     loop.run_until_complete(daemon.run())
#     logger.warn('Shiva is stopped.')
