import typer
# from art import tprint
from shiva.art import logo
from shiva.main import main

name = 'daemon'
help_text = 'Shiva common commands'
command = typer.Typer()


@command.command('')
def run(config: str = '', application: str = 'shiva_default'):
    """
        Run shiva daemon
    """
    # tprint('Shiva')
    print(logo())
    print('Starting shiva...')
    print(f'Starting shiva APP: {application} ...')
    main(config)
