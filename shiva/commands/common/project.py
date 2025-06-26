import typer
from loguru import logger

name = 'project'
help_text = 'Shiva project helper commands'
command = typer.Typer()


@command.command('')
def init():
    """
        Init shiva project
        Create base folders
    """
    logger.info('Initialize started...')
