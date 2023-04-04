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
    

@app.command("add_book")
def add_book():
    """Adds a new book to the library"""
    
    typer.secho(f"Sign in first to add a new book", fg=typer.colors.GREEN)
    username = input("Enter username: ")
    password = int(input("Enter password: "))
    if signIn(username, password):
        typer.secho(f"Please enter the required book info to add!", fg=typer.colors.BLUE)
        name = input("Name: ")
        author = input("Author: ")
        pages = int(input("# Pages: "))
        genre = input("Genres: ")
        
        addBook(name, author, pages, genre)
        typer.secho(f"Seccuessfully added book!", fg=typer.colors.GREEN)
        
    else:
        typer.secho(f"Please sign in again!", fg=typer.colors.RED)

@app.command("borrow_book")
def borrow_book(id: int):
    typer.secho(f"Sign in first to borrow book", fg=typer.colors.GREEN)
    borrowBook(id)

    
@app.command("return_book")
def return_book(id: int):
    typer.secho(f"Sign in first to return book", fg=typer.colors.GREEN)
    returnBook(id)
    
@app.command("mark_read")
def mark_read(id: int):
    typer.secho(f"Sign in first to mark book as read", fg=typer.colors.GREEN)
    markRead(id)
    
@app.command("fav_book")
def fav_book(id: int):
    typer.secho(f"Sign in first to mark book as read", fg=typer.colors.GREEN)
    favBook(id)


@app.command("my_books")
def my_books():
    try:
        typer.secho(f"Sign in first to show books", fg=typer.colors.GREEN)
        username = input("Username: ")
        password = int(input("Password: "))
        
        if signIn(username, password):
            books = readBooks(username)
            typer.secho(f"BOOKS YOU READ")
            display_table(books)
            books2 = favoriteBooks(username)
            typer.secho(f"YOUR FAVORITE BOOKS")
            display_table(books2)
        else:
            typer.secho(f"Sign in again!")
    except (ValueError,AttributeError) as e:
        typer.echo(f'Sign in again!', e)

@app.command("search_by_name")
def search_by_name(name : str) :
    typer.echo(f"lets search about {name}")
    Search_by_name(name)

@app.command("search_by_author")
def search_by_author(author : str):
    typer.echo(f"lets search using author {author}")
    Search_by_author(author)

@app.command("recently_added")
def recently_added():
        typer.echo(f"lets see which book recently added")
        Recently_added()


# Example function for tables, you can add more columns/row
def display_table(books):

    table = Table(show_header=True, header_style="bold blue")
   
    table.add_column("Book ID", style="dim", min_width=10, justify=True)
    table.add_column("Book Name", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Pages", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Availability", style="dim", min_width=10, justify=True)

    
    for book in books:
        table.add_row(str(book[0]),book[1], book[2], str(book[3]), book[4], str(book[5]))
    
    console.print(table)

if __name__ == "__main__":
    app()

