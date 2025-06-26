from loguru import logger
from shiva.common.modules_helper import get_class_that_defined_method


class Router:
    def __init__(self):
        self.routes = {}
        self.func_names = set()

    def route(self, *args):
        def wrapper(fnc):
            if fnc.__name__ in self.func_names:
                logger.error(f'Function already loaded: {fnc.__name__}. Check conflicting names. (Class: {fnc.__qualname__.split(".")[0]})')

            for r in args:
                self.routes[r] = fnc.__name__
            self.func_names.add(fnc.__name__)
            return fnc
        return wrapper
