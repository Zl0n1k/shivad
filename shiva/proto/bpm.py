import datetime
import uuid
from collections import defaultdict
from copy import deepcopy

import orjson
from aio_pika import Message
from loguru import logger
from shiva.common.base import BaseProtocol
from shiva.const import MSG_ACK, MSG_NACK, MSG_REJECT

# {
#     "action": "all",
#     "object": "location",
#     "params": {
#         "data": [
#             {
#                 "id": "T_CN_CAN_CRR",
#                 "name": "Гуанчжоу (Guangzhou), депо CRRC",
#                 "type": "Терминал",
#                 "subtype": "Депо",
#                 "depo_region": "AE_CN_CAN"
#             }
#         ]
#     },
#     "priority": 1,
#     "system_to": "bpm",
#     "message_id": "de897640-1439-4eeb-a2a9-da14f081f55e",
#     "api_version": "1.0",
#     "system_from": "catalog",
#     "reference_id": "71967781",
#     "datetime_created": "2021-03-10 11:00:26.816493"
# }

MSG_TEMPLATE = {
    "system_from": None,
    "system_to": None,
    "object": None,
    "action": None,
    "reference_id": None,
    "message_id": None,
    "params": {
    },
    "priority": 1,
    "api_version": "1.0",
    "datetime_created": None
}


MSG_REPLY_TEMPLATE = {
    "system_from": None,
    "system_to": None,
    "object": None,
    "action": None,
    "reference_id": None,
    "message_id": None,
    "params": {
        'status': {
            'success': True,
            'request_id': None,
            'errors': []
        },
    },
    "priority": 1,
    "api_version": "1.0",
    "datetime_created": None
}


class RoutedPublisher:
    def __init__(self, exchange, system_from, msg_source={}):
        self.exchange = exchange
        self.system_from = system_from
        self.msg_source = msg_source

    async def publish(self, system_to, m_object, action, params={}, reference_id=None, route_key=None, success=True, errors=[]):
        if not route_key:
            route_key = f'{m_object}.{action}'
        msg_id = uuid.uuid4()

        if not reference_id:
            reference_id = msg_id
        data = deepcopy(MSG_TEMPLATE)
        data['system_from'] = self.system_from
        data['system_to'] = system_to
        data['message_id'] = msg_id
        data['reference_id'] = reference_id
        data['datetime_created'] = datetime.datetime.utcnow().isoformat(timespec='seconds')
        data['object'] = m_object
        data['action'] = action
        data['params'].update(params)
        await self.exchange.publish(Message(orjson.dumps(data)), route_key)
        logger.info(f'[publisher] Message sended: {route_key}')

    async def publish_reply(self, msg, success=True, errors=[]):
        route_key = f'{self.msg_source["object"]}.{self.msg_source["action"]}_reply'
        msg_id = uuid.uuid4()
        data = {
            "system_from": self.msg_source['system_to'],
            "system_to": self.msg_source['system_from'],
            "object": self.msg_source['object'],
            "action": f'{self.msg_source["action"]}_reply',
            "reference_id": self.msg_source['reference_id'],
            "message_id": msg_id,
            "params": {
                'status': {
                    'success': success,
                    'request_id': self.msg_source['message_id'],
                    'errors': errors
                },
            },
            "priority": 1,
            "api_version": "1.0",
            "datetime_created": datetime.datetime.utcnow().isoformat(timespec='seconds')
        }
        if msg:
            data['params'].update(msg)

        # if self.msg_source.get('reference_id'):
        #     data['reference_id'] = self.msg_source['reference_id']
        # else:
        #     data['reference_id'] = msg_id
            
        # if self.msg_source.get('message_id'):
        #     data['params']['status']['request_id'] = self.msg_source['message_id']

        await self.exchange.publish(Message(orjson.dumps(data)), route_key)
        logger.info(f'[publisher_reply] Message sended: {route_key}')


class JSON_Routed_BPM(BaseProtocol):
    def __init__(self, *args, exchanges=None):
        super().__init__(*args)
        self.exchanges = exchanges
        self.routes = {}

    async def prepare(self):
        routes = defaultdict(list)

        # TODO: Handle with responces and exchanges
        for k, v in self.exchanges.items():
            self.default_exchange = v
            break

        for w, inst_all in self.workers.items():
            for i in inst_all:
                if i:
                    # i = inst[0]
                    i.exchanges = self.exchanges

                    # Default exchange
                    i.default_exchange = self.default_exchange
                    # routes:
                    if hasattr(i, 'router'):
                        for r_name, fnc_name in i.router.routes.items():
                            routes[r_name].append(getattr(i, fnc_name))
                            logger.info(f'Routing loaded: {r_name}')
                    else:
                        logger.error(f'[JSON_Routed_BPM] class: {i.__class__.__name__} router REQUIRED!')
        for k, l in routes.items():
            self.routes[k] = tuple(l)

        # TODO: Handle with responces and exchanges
        for k, v in self.exchanges.items():
            self.default_exchange = v
            break

    async def reply(self, msg, msg_src):
        route_key = f'{msg_src["object"]}.{msg_src["action"]}_reply'
        publisher = RoutedPublisher(self.default_exchange, msg_src['system_to'], msg_src)
        await publisher.publish_reply(msg)

        # async def publish_reply(self, system_to, m_object, action, params={}, route_key=None, success=True, errors=[]):
        # msg_id = uuid.uuid4()
        # data = {
        #     "system_from": msg_src['system_to'],
        #     "system_to": msg_src['system_from'],
        #     "object": msg_src['object'],
        #     "action": f'{msg_src["action"]}_reply',
        #     "reference_id": msg_src['message_id'],
        #     "message_id": msg_id,
        #     "params": {
        #         'status': {
        #             'success': True,
        #             'request_id': None,
        #             'errors': []
        #         },
        #     },
        #     "priority": 1,
        #     "api_version": "1.0",
        #     "datetime_created": datetime.datetime.utcnow().isoformat(timespec='seconds')
        # }
        # if msg:
        #     data['params'].update(msg)
        # await self.default_exchange.publish(Message(orjson.dumps(data)), route_key)
        logger.info(f'Message sended: {route_key}')

    async def on_error(self, msg_raw, error):
        pass

    async def dispatch(self, msg):
        msg_json = orjson.loads(msg.body)
        p_key = self.get_p_key(msg_json)
        logger.info(f'Dispatching[{self.__class__}] {p_key}')
        # logger.info(self.routes)
        for f in self.routes.get(p_key, []):
            try:
                reply = await f(msg_json['params'])
                if reply:
                    await self.reply(reply, msg_json)
            except Exception:
                logger.exception(f'Unable to process message: {p_key}: {f}')

    def get_p_key(self, msg):
        p_key = None
        try:
            p_key = f'{msg["object"]}.{msg["action"]}'
        except Exception:
            logger.exception(f'Unable to get p_key: {msg}')
        return p_key
