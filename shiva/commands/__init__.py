import typer

app = typer.Typer()


@app.command()
def word(word: str, second: str = 'default'):
    """
        Some help string
    """
    print(f'WORD: {word}')


@app.command()
def word_1(word: str):
    print(f'WORD: {word}')
