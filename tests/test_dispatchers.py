from shiva.dispatchers import web


class DummyShiva:
    pass


def test_web_dispatcher_router_registration():
    shiva = DummyShiva()
    config = {}
    dispatcher_config = {"name": "dispatcher_web"}
    dispatcher = web.Web(shiva, config, dispatcher_config)
    assert dispatcher.name == "dispatcher_web"
