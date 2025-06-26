import asyncio

from loguru import logger
from prometheus_client import Counter, Gauge

from shiva.common.base import BaseMetric


class MyMetric(BaseMetric):
    name = 'my_metric'
    dispatcher = 'metrics_main'

    async def prepare(self):
        logger.info('Starting main metrics')

    async def start(self):
        logger.info('Metrics started!')
        g = Gauge('my_gauge_metric', 'Some metric')
        c = Counter('my_shit', 'test_counter')
        self.running = True
        while self.running:
            g.inc()
            logger.info('Metrics sleep...')
            c.inc(1.2)
            await asyncio.sleep(5)
    async def stop(self):
        self.running = False
