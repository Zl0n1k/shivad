import typer

name = 'maintest'
help_text = 'Shiva tests'
command = typer.Typer()


@command.command()
def test(word: str, second: str = 'default'):
    """
        Test commands
    """
    print(f'WORD: {word}')


@command.command()
def test_1(word: str):
    print(f'WORD: {word}')
