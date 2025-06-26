import asyncio
import time

from aio_pika import Message
from aio_pika.exceptions import ChannelClosed, ChannelInvalidStateError, QueueEmpty
from aio_pika.pool import Pool
from loguru import logger

from shiva.common.base import BaseDispatcher, BaseProtocol, BaseRmqWorker
from shiva.const import MODULES_WORKERS, MSG_ACK, MSG_NACK, MSG_REJECT


class RmqDispatcher(BaseDispatcher):
    name = "rmq"
    base_class = BaseRmqWorker

    # async def load(self, workers_scope):

    async def prepare(self):
        self.running = False
        self.exchanges = {}
        self.queues = {}
        self.channels = []
        self.queue_iters = []
        self.connection_class = self.shiva.connections[self.dispatcher_config["connection"]]
        self.proto = None
        logger.warning(f"Preparing: {self.name}...")
        logger.info(f"Connection: {self.dispatcher_config['connection']}: {self.connection_class}")
        self.connection = await self.connection_class.get_connection()
        logger.info("Connected!")
        await self.init_exchanges()
        await self.load_proto()

    async def load_proto(self):
        for c in self.shiva.scopes["proto"].filter_members(BaseProtocol):
            if c.__name__ == self.dispatcher_config["proto"]:
                self.proto = c(self.shiva, self.workers, exchanges=self.exchanges)
                await self.proto.prepare()
                logger.info(
                    f"[{self.__class__.__name__}][{self.dispatcher_config['name']}] Loading protocol: {c.__name__}"
                )

    async def init_exchanges(self):
        logger.info("Init exchanges...")
        for exch_name, config in self.dispatcher_config["config"]["exchanges"].items():
            logger.info(f"Configuring exchange: {exch_name}")
            # V2
            v2_enabled = False
            v2_system = None
            if config.get("routing"):
                if config["routing"].get("v2_enabled") and config["routing"].get("system"):
                    v2_enabled = config["routing"]["v2_enabled"]
                    v2_system = config["routing"]["system"]

            # Exchange only channel
            exch_chan = await self.connection.channel(**config.get("config_channel", {}))
            self.channels.append(exch_chan)
            exchange = await exch_chan.declare_exchange(exch_name, **config["config"])
            self.exchanges[exch_name] = exchange
            if config.get("queues"):
                for q_name, q_cfg in config["queues"].items():
                    self.queues[q_name] = []
                    # Separate channels for queues
                    coro = 1
                    if q_cfg.get("coro"):
                        coro = q_cfg["coro"]
                    for coro_num in range(coro):
                        q_chan = await self.connection.channel()
                        if q_cfg["config"].get("prefetch") is not None:
                            await q_chan.set_qos(prefetch_count=int(q_cfg["config"]["prefetch"]))
                        self.channels.append(q_chan)
                        exchange = await q_chan.declare_exchange(exch_name, **config["config"])
                        queue = await q_chan.declare_queue(
                            q_name, **q_cfg["config"]["arguments"], arguments=q_cfg["config"].get("additional", {})
                        )
                        for bind in q_cfg["bindings"]:
                            logger.info(f"Binding {q_name}->{exch_name}: {bind}")
                            await queue.bind(exchange, bind)
                            # V2 binding
                            if v2_enabled:
                                v2_binding = f"{bind}.{v2_system}"
                                logger.info(f"Binding(v2) {q_name}->{exch_name}: {v2_binding}")
                                await queue.bind(exchange, v2_binding)
                        self.queues[q_name].append(queue)

    async def start(self):
        if self.workers:
            # Run start function
            for w_name, workers in self.workers.items():
                for w in workers:
                    await w.start()
                    logger.info(f"Starting worker {w_name}...")
            self.running = True
            logger.warning(f"Starting {self.name}({self.dispatcher_config['name']})")
            for q_name, channel_list in self.queues.items():
                logger.warning(f"Starting queue {q_name} with {len(channel_list)} coro...")
                coro_num = 0
                for c in channel_list:
                    self.coro.append(self.consumer(q_name, c, coro_num))
                    # self.coro.append(self.consumer_get_method(q_name, c, coro_num))
                    coro_num += 1

    async def consumer_get_method(self, q_name, q_obj, coro_num):
        logger.warning(f"Starting[get] {q_name}[{coro_num}]")
        while self.running:
            try:
                msg = None
                try:
                    msg = await q_obj.get(timeout=2)
                except QueueEmpty:
                    await asyncio.sleep(0.3)
                if self.running and msg:
                    s = time.time()
                    try:
                        await self.proto.dispatch(msg)
                    except Exception:
                        logger.exception(f"Unable to process message for proto: {self.proto}")
                    await msg.ack(multiple=True)
                    logger.info(f"[{coro_num}][get] Message consumed in: {time.time() - s}")
            except Exception:
                logger.exception("[get][{q_name}][{coro_num}] Unable to handle message")
        logger.warning(f"[get]Stopped: {q_name}[{coro_num}]")

    async def consumer(self, q_name, q_obj, coro_num):
        logger.warning(f"Starting {q_name}[{coro_num}]")
        try:
            async with q_obj.iterator() as queue_iter:
                self.queue_iters.append(queue_iter)
                async for message in queue_iter:
                    # Unhandled err
                    try:
                        if self.running:
                            s = time.time()
                            # Return values: MSG_ACK, MSG_NACK, MSG_REJECT
                            msg_action = MSG_ACK
                            try:
                                msg_act = await self.proto.dispatch(message)
                                if msg_act is not None:
                                    msg_action = msg_act
                            except Exception:
                                logger.exception(f"Unable to process message for proto: {self.proto}")
                            if msg_action == MSG_ACK:
                                await message.ack()
                            elif msg_action == MSG_NACK:
                                await message.nack()
                            elif msg_action == MSG_REJECT:
                                await message.reject()
                            logger.info(f"[{coro_num}] Message consumed(FLAG: {msg_action}) in: {time.time() - s}")
                    except (ChannelClosed, ChannelInvalidStateError) as e:
                        logger.error(f"Channel error: {e}. Stopping Shiva!")
                        self.shiva.stop()
        except Exception as err:
            logger.error(err)
        logger.warning(f"Stopped: {q_name}[{coro_num}]")

    async def stop(self):
        self.running = False
        logger.warning("Shutting down queue iters...")
        for i in self.queue_iters:
            logger.info(f"Stopping iter: {i}")
            await i.close()
        logger.warning("Shutting down channels...")
        for ch in self.channels:
            logger.warning(f"Closing channel: {ch}")
            await ch.close()
        logger.warning(f"Shutting down connection {self.connection}...")
        await self.connection.close()
        logger.warning(f"Connection closed {self.connection}...")
        for w_name, w_obj in self.workers.items():
            logger.warning(f"Stopping rmq worker: {w_name}")
            if hasattr(w_obj, "stop"):
                await w_obj.stop()
