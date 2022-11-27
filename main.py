import typer
from rich.console import Console
from rich.table import Table
from typing import Optional

console = Console()

app = typer.Typer()

@app.command("start")
def start():
    typer.secho(f'''Welcome to Library CLI!\n\n
        You can execute command '--help' to see the possible commands''', fg=typer.colors.GREEN)
    # TODO: connect to database

# This is how you can get arguments, here username is a mandatory argument for this command.
@app.command("sign_up")
def sign_up(username: str):
    typer.echo(f"Nice that you are signing up!")
    # TODO: Add user with name {username} to database table

# Example function for tables, you can add more columns/row.
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

