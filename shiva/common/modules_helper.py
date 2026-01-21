import functools
import importlib
import inspect
import os
import pkgutil
from collections import defaultdict

from loguru import logger


def get_class_that_defined_method(meth):
    if isinstance(meth, functools.partial):
        return get_class_that_defined_method(meth.func)
    if inspect.ismethod(meth) or (
        inspect.isbuiltin(meth)
        and getattr(meth, "__self__", None) is not None
        and getattr(meth.__self__, "__class__", None)
    ):
        for cls in inspect.getmro(meth.__self__.__class__):
            if meth.__name__ in cls.__dict__:
                return cls
        meth = getattr(meth, "__func__", meth)  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth), meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0], None)
        if isinstance(cls, type):
            return cls
    return getattr(meth, "__objclass__", None)  # handle special descriptor objects


class ModuleHelper:
    def __init__(self):
        self.module = None
        self.path = None

    def load_path(self, path):
        try:
            self.module = importlib.import_module(path)
            self.path = path
            return self.module
        except ModuleNotFoundError:
            # Not critical - package/module may not exist
            logger.debug(f"Module path not found (skipping): {path}")
            return None
        except Exception as err:
            # Critical error - module exists but failed to load
            logger.error(f"Unable to import path: {path}: {err}")
            return None

    def load_module(self, module):
        self.module = module
        return self.module

    def get_libs(self, package=None, user_scope=False):
        modules = []
        if not package:
            package = self.module
        submodules = pkgutil.walk_packages(package.__path__, package.__name__ + ".")
        for loader, module_name, is_pkg in submodules:
            # print(f'Module: {module_name}')
            # logger.debug(f'{loader} : {module_name} : {is_pkg}')
            try:
                module = importlib.import_module(module_name)
                if not is_pkg or user_scope:
                    modules.append(module)
            except Exception as e:
                logger.exception(f"Unable to load library: {module_name}: {e}")
        return modules


class Scope:
    def __init__(self, scope_name: str, scopes: list):
        self.scope_name = scope_name
        self.scopes = []
        self.scopes_raw = scopes
        self.load()

    def load(self):
        """
        Load modules from scope paths.

        Note: Duplicates are filtered by module file path.
        First found module wins - later modules with same file are skipped.
        TODO: If override behavior needed (user > packages > shiva),
        reverse the scopes_raw list before loading.
        """
        loaded_files = []
        for scope in self.scopes_raw:
            mh = ModuleHelper()
            success = mh.load_path(scope)
            if success:
                libs = mh.get_libs()
                loaded_count = 0
                for m in libs:
                    if m.__file__ not in loaded_files:
                        self.scopes.append(m)
                        loaded_files.append(m.__file__)
                        loaded_count += 1
                if loaded_count > 0:
                    logger.debug(f"Loaded {loaded_count} modules from: {scope}")
            else:
                # Module path not found - already logged in load_path
                pass

    def filter_members(self, base_class):
        classes = []
        for m in self.scopes:
            members = inspect.getmembers(m, inspect.isclass)
            for member in members:
                action_name, action_class = member
                if issubclass(action_class, base_class) and action_class != base_class:
                    if hasattr(action_class, "load_globals"):
                        # print('---------LOADING--------')
                        for var_name in action_class.load_globals:
                            if hasattr(m, var_name):
                                setattr(action_class, var_name, getattr(m, var_name))
                    classes.append(action_class)
        return classes

    def filter_objects(self, base_class):
        classes = []
        for m in self.scopes:
            members = inspect.getmembers(m, inspect.ismemberdescriptor)
            for member in members:
                action_name, action_class = member
                # print(f'{action_name}: {action_class}')
                if issubclass(action_class, base_class) and action_class != base_class:
                    classes.append(action_class)
                #     if action_class.dispatcher in self.dispatchers.values():
                #         logger.info(f'Action "{action_class}" imported!')
                #         self.actions[action_class.dispatcher.name].append(action_class)
        return classes
