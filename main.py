import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from database import *

console = Console()

app = typer.Typer()

@app.command("start")
def start():
    """This command creats and connects to the database"""
    typer.secho(f'''Welcome to Library CLI!\n\n
        You can execute command '--help' to see the possible commands''', fg=typer.colors.GREEN)
    connect()

# This is how you can get arguments, here username is a mandatory argument for this command.
@app.command("sign_up")
def sign_up(username: str, password: int):
    """This command allows the user to sign up"""
    typer.echo(f"Nice that you are signing up!")
    singUp(username, password)
    
# This is to sign in the user
@app.command("sign_in")
def sign_in(username: str, password: int):
    typer.echo(f"Nice that you are signing in!")
    signIn(username, password) 
    

@app.command("add_book")
def add_book():
    """This command adds a new book to the library"""
    
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
    """This command allows the user to borrow a book from the library"""
    typer.secho(f"Sign in first to borrow book", fg=typer.colors.GREEN)
    borrowBook(id)

    
@app.command("return_book")
def return_book(id: int):
    """This command allows the user to return a book to the library"""
    typer.secho(f"Sign in first to return book", fg=typer.colors.GREEN)
    returnBook(id)
    
@app.command("mark_read")
def mark_read(id: int):
    """This command allows the user to mark a book as read"""
    typer.secho(f"Sign in first to mark book as read", fg=typer.colors.GREEN)
    markRead(id)
    
@app.command("fav_book")
def fav_book(id: int):
    """This command allows the user to add books to their favorite list"""
    typer.secho(f"Sign in first to mark book as read", fg=typer.colors.GREEN)
    favBook(id)


@app.command("my_books")
def my_books():
    """This command gives a summary of the books the user has read and their book favorite list"""
    try:
        # sign in the user first to show the books they have read and their book favorite list
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
def search_by_name(name : str):
    """This command allows the user to search for a book by its name"""
    typer.echo(f"lets search about {name}")
    Search_by_name(name)

@app.command("search_by_author")
def search_by_author(author : str):
    """This command allows the user to search for a book by author's name"""
    typer.echo(f"lets search using author {author}")
    Search_by_author(author)

@app.command("recently_added")
def recently_added(genre : Optional[str]= typer.Argument("")):
    """This command shows the user the books that were recently added"""
    typer.echo(f"lets see which book recently added")
    Recently_added(genre)


@app.command("most_read_books")
def most_read_books(genre : Optional[str]= typer.Argument("")):
    """This command shows the user their most read books and how many times they read the book"""
    books = mostReadBooks(genre)
    table = Table(show_header=True, header_style="bold blue")
   
    table.add_column("#", style="dim", min_width=10, justify=True)
    table.add_column("Book ID", style="dim", min_width=10, justify=True)
    table.add_column("Book Name", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Times read", style="dim", min_width=10, justify=True)

    for i,book in enumerate(books):
        table.add_row(str(i+1),str(book[0]),book[1], book[2], book[3], str(book[4]))
    
    console.print(table)




@app.command("statistics")
def Statistics():
    """This command shows a statistics of books, authors, genres and no. of pages the user has read"""
    try :
        typer.secho(f"Sign in first to show statistics about user", fg=typer.colors.GREEN)
        username = input("Username: ")
        password = int(input("Password: "))
        
        if signIn(username,password):
            stats = statestics(username)
            table = Table(show_header=True, header_style="bold blue")
   
            table.add_column("Statistics", style="dim", min_width=10, justify=True)
            table.add_column("Numbers", style="dim", min_width=10, justify=True)
            
            names = ['Books you read', 'Authors you read', 'Genres you read', 'Total pages you read']
            
            for i,j in enumerate(zip(stats)):
                table.add_row(names[i],str(*j[0]))
                
            console.print(table)

    
    except (ValueError,AttributeError, psycopg2.DatabaseError) as e:
        typer.echo(f'Sign in failed!', e)

@app.command("most_favorite_books")
def most_read_books(genre : Optional[str]= typer.Argument("")):
    """This command shows the user their most favorite books and how many times they read the book"""
    books = Most_favorite_books(genre)
    table = Table(show_header=True, header_style="bold blue")
   
    table.add_column("#", style="dim", min_width=10, justify=True)
    table.add_column("Book ID", style="dim", min_width=10, justify=True)
    table.add_column("Book Name", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Times read", style="dim", min_width=10, justify=True)

    for i,book in enumerate(books):
        table.add_row(str(i+1),str(book[0]),book[1], book[2], book[3], str(book[4]))
    
    console.print(table)


@app.command("most_read_author")
def most_read_author():
    """This command shows the user their most favorite books and how many times they read the book"""
    books = Most_read_author()
    table = Table(show_header=True, header_style="bold blue")
   
    table.add_column("#", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Count", style="dim", min_width=10, justify=True)

    for i,book in enumerate(books):
        table.add_row(str(i+1),book[0],str(book[1]))
    
    console.print(table)

@app.command("most_read_genres")
def most_read_genres():
    """This command shows the user their most read genres and how many times they read them"""
    books = mostReadGenres()
    
    table = Table(show_header=True, header_style="bold blue")
   
    table.add_column("#", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Count", style="dim", min_width=10, justify=True)
    
    for i,book in enumerate(books):
        table.add_row(str(i+1),book[0],str(book[1]))
        
    console.print(table)
    
    



    

# function for tables, you can add more columns/row
def display_table(books):

    table = Table(show_header=True, header_style="bold blue")
    
    table.add_column("#", style="dim", min_width=10, justify=True)
    table.add_column("Book ID", style="dim", min_width=10, justify=True)
    table.add_column("Book Name", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Pages", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Availability", style="dim", min_width=10, justify=True)

    
    for i, book in enumerate(books):
        table.add_row(str(i+1),str(book[0]),book[1], book[2], str(book[3]), book[4], str(book[5]))
    
    console.print(table)

if __name__ == "__main__":
    app()

