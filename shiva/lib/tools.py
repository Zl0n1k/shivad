import os

import yaml
from mako.template import Template


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Config(Singleton):
    def __init__(self, config_path: str) -> None:
        self.path = config_path
        self.config = None

    def get_config(self) -> dict:
        if not self.config:
            with open(self.path, encoding="utf8") as f:
                cfg_raw = f.read()
                cfg_tmpl = Template(cfg_raw, strict_undefined=True)
                cfg_final = cfg_tmpl.render(**os.environ)
                self.config = yaml.load(cfg_final, Loader=yaml.SafeLoader)
        return self.config