import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def hello(name: str):
    """Say hello to NAME"""
    console.print(f"Hello {name}")

@app.command()
def goodbye(name: str, formal: bool = False):
    """Say goodbye to NAME"""
    if formal:
        console.print(f"Goodbye {name}. It was a pleasure.")
    else:
        console.print(f"Bye {name}!")

if __name__ == "__main__":
    app()