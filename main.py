import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from database import *

console = Console()

app = typer.Typer()

@app.command("start")
def start():
    typer.secho(f'''Welcome to Library CLI!\n\n
        You can execute command '--help' to see the possible commands''', fg=typer.colors.GREEN)
    connect()

# This is how you can get arguments, here username is a mandatory argument for this command.
@app.command("sign_up")
def sign_up(username: str, password: int):
    typer.echo(f"Nice that you are signing up!")
    singUp(username, password)
    
# This is to sign in the user
@app.command("sign_in")
def sign_in(username: str, password: int):
    typer.echo(f"Nice that you are signing in!")
    signIn(username, password)

@app.command("search_by_name")
def search_by_name(name : str) :
    typer.echo(f"lets search about {name}")
    Search_by_name(name)

@app.command("search_by_author")
def search_by_author(author : str):
    typer.echo(f"lets search using author {author}")
    Search_by_author(author)

@app.command()
def borrow_book():
    pass
    # 
    # 
    # 
    # 
    

# Example function for tables, you can add more columns/row
@app.command("display_table")
def display_table():
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Column 1", style="dim", width=10)
    table.add_column("Column 2", style="dim", min_width=10, justify=True)
    
    table.add_row('Value 1', 'Value 2')
    table.add_row('Value 3', 'Value 4')
    table.add_row('Value 5', 'Value 6')

    console.print(table)

if __name__ == "__main__":
    app()

