import prometheus_client
from loguru import logger
from prometheus_client import Gauge, make_asgi_app

from shiva.common.base import BaseDaemon, BaseDispatcher, BaseMetric


class MetricsRoot(BaseDispatcher):
    name = 'metrics_root'
    base_class = BaseMetric

    async def prepare(self):
        self.metrics_app = make_asgi_app()
        if self.dispatcher_config.get('unregister_defaults'):
            prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
            prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
            prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)
        if self.workers:
            logger.info(f'Mounting metrics main: {self.dispatcher_config["uri"]}')
            self.shiva.app.mount(self.dispatcher_config['uri'], self.metrics_app)
        
    async def start(self):
        for d_name, d_list in self.workers.items():
            logger.info(f'Running {d_name}')
            for w in d_list:
                self.coro.append(w.start())

    async def stop(self):
        for d_name, d_list in self.workers.items():
            logger.warning(f'Stopping {d_name}')
            for w in d_list:
                for d in d_list:
                    await d.stop()
        logger.warning(f'Stopped: {self.name}')
