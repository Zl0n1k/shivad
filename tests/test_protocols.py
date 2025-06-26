from shiva.proto.rmq_simple import JSON_UnroutedALL
from shiva.proto.bpm import RoutedPublisher
from unittest.mock import MagicMock, AsyncMock
import pytest


class DummyShiva:
    pass


class DummyWorker:
    async def run(self, body):
        self.last_body = body


@pytest.mark.asyncio
async def test_json_unroutedall_dispatch():
    shiva = DummyShiva()
    config = {}
    proto = JSON_UnroutedALL(shiva, config)
    worker = DummyWorker()
    proto.routes = {"w1": worker}

    class Msg:
        body = {"foo": "bar"}

    await proto.dispatch(Msg())
    assert worker.last_body == {"foo": "bar"}


@pytest.mark.asyncio
async def test_routed_publisher_publish():
    exchange = MagicMock()
    exchange.publish = AsyncMock()
    proto = RoutedPublisher(exchange, "system_from")
    await proto.publish("system_to", "object", "action", params={})
    exchange.publish.assert_awaited()
