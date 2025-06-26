import importlib

import typer
from loguru import logger
from shiva import commands
from shiva.common.modules_helper import ModuleHelper
from shiva.const import MODULES_COMMANDS


class CommandHelper:
    def __init__(self):
        self.command = typer.Typer()
        import os
        print(os.getcwd())

    def _load_commands(self, mh_com, user_scope=False):
        objects = mh_com.get_libs(user_scope=user_scope)
        logger.info(f'Found {len(objects)} command packages. Discovering...')
        for cmd_root in objects:
            if hasattr(cmd_root, 'command'):
                name = None
                if hasattr(cmd_root, 'name'):
                    name = cmd_root.name
                    logger.info(f'Loading commands group: {cmd_root.name}')
                    self.command.add_typer(cmd_root.command, name=name, help=cmd_root.help_text)
                else:
                    logger.info(f'Loading single commands: {cmd_root.__name__}')
                    self.command.add_typer(cmd_root.command)
        logger.info('Shiva commands successfuly loaded.')

    def load_user(self):
        logger.info('Discovering users commands...')
        mh_com = ModuleHelper()
        try:
            module = importlib.import_module(MODULES_COMMANDS)
            mh_com.load_module(module)
            self._load_commands(mh_com, user_scope=True)
        except ModuleNotFoundError:
            logger.info(f"Can't find module '{MODULES_COMMANDS}' with users commands")

    def load_common(self):
        logger.info('Discovering shiva internal commands...')
        mh_com = ModuleHelper()
        mh_com.load_module(commands)
        self._load_commands(mh_com)
