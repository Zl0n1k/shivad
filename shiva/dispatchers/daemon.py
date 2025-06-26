from loguru import logger
from shiva.common.base import BaseDaemon, BaseDispatcher


class DaemonRoot(BaseDispatcher):
    name = 'daemon_root'
    base_class = BaseDaemon

    async def prepare(self):
        # print('*' * 80)
        # print(self.workers_configurations)
        # print(self.workers_all)
        # print(self.workers)
        # print('*' * 80)
        pass
        
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
