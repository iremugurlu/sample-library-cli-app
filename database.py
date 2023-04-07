import psycopg2
import typer
from rich.console import Console
from rich.table import Table
import datetime

from config import config

console = Console()
def connect():
    conn = None
    try:
        try:
            # try to connect to database
            params = config('database.ini','CLI_Library')
            conn = psycopg2.connect(**params)
		
            # create a cursor
            cur = conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            # if database doesn't exist, create it
            try:
                params = config('database.ini','postgres')
                conn = psycopg2.connect(**params)
                conn.autocommit = True # this command enables autocommit to postgreSQL otherwise at the end of each operation you must do conn.commit()
                cur = conn.cursor()
                
                cur.execute("CREATE DATABASE cli_library;")
                typer.secho(f"Database created successfully", fg=typer.colors.GREEN)
                
            except psycopg2.Error as e:
                # If the CREATE DATABASE statement fails or another error occurs, catch the exception and print an error message
                typer.echo(f"The CREATE DATABASE statement failed: {e}")
                
            else:
                # Create tables after the CREATE DATABASE statement
                params = config('database.ini','CLI_Library')
                conn = psycopg2.connect(**params)
                conn.autocommit = True
                curr = conn.cursor()
                curr.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            
                file = open('cli_library.sql', 'r')
                sqlFile = file.read()
                file.close()
                sqlCommands = sqlFile.split(';')[:-1]
                # Execute every command from the input file
                for command in sqlCommands:
                    try:
                        curr.execute(command)
                    except (Exception, psycopg2.DatabaseError) as error:
                        print("Command skipped: ", error)
                        break
                conn.close()
                cur.close()
            
            
        else:
            # If the database exists and tables don't exist, then create tables
            conn.autocommit = True 
            curr = conn.cursor() 
            curr.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            table_names = curr.fetchall()
            
            if len(table_names) != 0:
                pass
                    
            else:
                file = open('cli_library.sql', 'r')
                sqlFile = file.read()
                file.close()
                sqlCommands = sqlFile.split(';')[:-1]
                # Execute every command from the input file
                for command in sqlCommands:
                    try:
                        curr.execute(command)
                    except (Exception, psycopg2.DatabaseError) as error:
                        print("Command skipped: ", error)
                        break
            
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurred, print the error
        print(error)    
                  
    finally: 
        # Close database connection
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    
from psycopg2.errors import UniqueViolation
from psycopg2 import errors

def singUp(username: str, password: int):
    ''' This function is called to sign up the user and store their information in the database'''
    # Connect to database
    params = config('database.ini','CLI_Library')
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('SELECT username FROM public."user";')
    
    # Check if the user is already in the database, else insert their information into the database
    user = list(*zip(*cur.fetchall()))
    while True:
        try:
            if username in  user:
                typer.secho(f"This user already exist! Try different user", fg=typer.colors.RED)
                username = input("Please Enter another username: ")
                continue
            else:   
                command = f'INSERT INTO "user" (username, password) VALUES (\'{username}\',\'{password}\');'
                cur.execute(command)
                cur.close()
                break
        
        except UniqueViolation as e:
            print("hi", e)
            username = input("Enter another username: ")
            continue
        

def signIn(username: str, password: int):
    '''This function is called to sign in the user and store their information accordingly'''
    try:
        # Connect to the database
        params = config('database.ini','CLI_Library')
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Collect usernames and passowrd of user
        cur.execute('SELECT username FROM public."user";')
        user = cur.fetchall()
        cur.execute('SELECT password FROM public."user";')
        user_pass = cur.fetchall()
        
        # if username or password entered correctly, sign the user in. else, show the error message
        for i,j in zip(user, user_pass):
            if username == i[0] and password == j[0]:
                typer.secho(f"You are signed in", fg=typer.colors.GREEN)
                # return True if sign in was successful
                success = True
                break
                
        else:
            typer.secho(f"username or password is wrong!", fg=typer.colors.RED)
            # return false if sign in was unsuccessful
            success = False
        
        return success
    except ValueError:
        print('Please Enter valid information')

def addBook(bookname: str, author: str, pages: int, genre: str):
    '''This function is called to add a book into the database'''
    try:
        try:
            # connect to the database
            params = config('database.ini','CLI_Library')
            conn = psycopg2.connect(**params)
            conn.autocommit = True
            cur = conn.cursor()
            
            # Select all books and authors names
            command_query = f''' SELECT name FROM books;
            SELECT author_name FROM author;'''.split('\n')
            
            # store all books and authors into a list
            queried_data = []
            for i in command_query:
                cur.execute(i)
                queried_data.append(cur.fetchall())
            
            # check of book and author names in the database, if exists add to the inventory without author namd and book name. else add them to database
            for i,j in zip(*queried_data):
                if i[0] == bookname and j[0] == author:
                    cur.execute(f'SELECT id FROM books WHERE name = \'{bookname}\'')
                    book_id = cur.fetchone()
                    command = f'''INSERT INTO inventory (book_id, last_update) VALUES (\'{int(book_id[0])}\',\'{datetime.date.today()}\');'''
                    cur.execute(command)
                    break
                elif i[0] != bookname and j[0] == author:
                    commandd = f'''INSERT INTO "books" (name,pages) VALUES (\'{bookname}\',\'{pages}\');
                    INSERT INTO "book_author" (book_id, author_id) VALUES ((SELECT id FROM "books" WHERE name = \'{bookname}\'), (SELECT id FROM "author" WHERE author_name = \'{author}\'));
                    INSERT INTO "inventory" (book_id, last_update) VALUES ((SELECT id FROM "books" WHERE name = \'{bookname}'), \'{datetime.date.today()}\');'''
                    cur.execute(commandd)
                    break            
            else:
                commandd = f'''INSERT INTO "books" (name,pages) VALUES (\'{bookname}\',\'{pages}\');
                INSERT INTO "author" (author_name) VALUES (\'{author}\');
                INSERT INTO "book_author" (book_id, author_id) VALUES ((SELECT id FROM "books" WHERE name = \'{bookname}\'), (SELECT id FROM "author" WHERE author_name = \'{author}\'));
                INSERT INTO "inventory" (book_id, last_update) VALUES ((SELECT id FROM "books" WHERE name = \'{bookname}'), \'{datetime.date.today()}\');'''
                cur.execute(commandd)
            
            # check if genre is already exists, else add it to avoid duplicate
            command = f'SELECT title FROM genre;'
            cur.execute(command)
            genre_title = cur.fetchall()
            
            
            for title in genre_title:
                if title[0] == genre:
                    pass
                    # command = f'INSERT INTO "genre_book" (book_id, genre_id) VALUES ((SELECT id FROM "books" WHERE name = \'{bookname}\'), (SELECT genre_id FROM "genre" WHERE title = \'{genre}\'));'
                    # cur.execute(command)
                    break

            else:
                cur.execute(f'INSERT INTO "genre" (title) VALUES (\'{genre}\');')
                command = f'INSERT INTO "genre_book" (book_id, genre_id) VALUES ((SELECT id FROM "books" WHERE name = \'{bookname}\'), (SELECT genre_id FROM "genre" WHERE title = \'{genre}\'));'
                cur.execute(command)
        except psycopg2.DatabaseError as e:
            print(e)

            
        
    except (SyntaxError, ValueError, psycopg2.DatabaseError) as e:
        typer.echo(f"Could not sign in", e)
        
        
def borrowBook(id: int):
    '''This function is called to borrow a book from the inventory to the borrowed book table'''
    # Takes the user's username and passwrod
    username = input("Username: ")
    password = int(input("Password: "))
    
    # sign in the user first to borrow book
    if signIn(username, password):
        # connect to database
        params = config('database.ini','CLI_Library')
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Select all books from inventory 
        cur.execute(f'SELECT book_id FROM inventory;')
        available_books = cur.fetchall()
        #  check of book exist to add it to the borrowed books table, else show that the table doesn't exist
        for book in available_books:
            if book[0] == id:
                print(book[0])
                command = f'''DELETE FROM inventory WHERE inventory_id IN (SELECT inventory_id FROM inventory WHERE book_id = {id} limit 1);
                INSERT INTO borrowed_books (book_id, username) VALUES (\'{id}\', \'{username}\');'''.split('\n')
                
                for i in command:
                    cur.execute(i)
                typer.secho(f'You borrowed book {id}!')
                break
        else:
            typer.secho('This book is not available')
           

    
def returnBook(id: int):
    '''This function is called to return a book to the inventory by the user'''
    username = input("Username: ")
    password = int(input("Password: "))

    # sign in the user first to allow them to return the book
    if signIn(username, password):
        params = config('database.ini','CLI_Library')
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        
        cur.execute(f'SELECT book_id FROM borrowed_books WHERE username = \'{username}\';')
        borrowed_books = cur.fetchall()
        
        # check if the user has borrowed the book, or add them back to the inventory
        for book in borrowed_books:
            if book[0] == id:
                command = f'''DELETE FROM borrowed_books WHERE bb_id IN (SELECT bb_id FROM borrowed_books WHERE book_id = {id} limit 1);
                INSERT INTO "inventory" (book_id, last_update) VALUES (\'{id}\', \'{datetime.date.today()}\'); '''
                cur.execute(command)
                typer.secho(f'You returned book {id}!')
                break
        else:
            typer.echo(f'You didn\'t borrow book {id}')
    else:
        typer.echo(f"Could not sign in")
            
            
            
def markRead(id: int):
    ''' this function is called to mark a book as read'''
    try:
        username = input("Username: ")
        password = int(input("Password: "))
        
        # sign in the user first to allow them to mark book as read
        if signIn(username, password):
            # connect to database
            params = config('database.ini','CLI_Library')
            conn = psycopg2.connect(**params)
            conn.autocommit = True
            cur = conn.cursor()
            
            cur.execute(f'SELECT id FROM books;')
            books = cur.fetchall()
            
            # check if the book exists in database and add it to the mark read table, if not display that the book doesn't exist
            for book in books:
                if book[0] == id:
                    command = f'INSERT INTO read_books (username, book_id) VALUES (\'{username}\', \'{id}\');'
                    cur.execute(command)
                    typer.secho(f'You marked book {id} as read!')
                    break
            else:
                typer.echo(f'Book {id} doesn\'t exist!')
        else:
            typer.echo(f"Could not sign in")
    except (ValueError,AttributeError) as e:
        typer.echo(f"Sign in failed",e)



def favBook(id: int):
    '''this function is called to add the book to the favorite book table'''
    username = input("Username: ")
    password = int(input("Password: "))
    
    # sign in the user first to allow them to add a book to their favorites
    if signIn(username, password):
        # connect to the database
        params = config('database.ini','CLI_Library')
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        
        cur.execute(f'SELECT id FROM books;')
        books = cur.fetchall()
        
        cur.execute(f'SELECT book_id, username FROM fav_books;')
        fav_books = zip(*cur.fetchall())
        
        
        fuser = []
        fbook = []
        for i,j in zip(*fav_books):
            fuser.append(j)
            fbook.append(i)
        
        # check if the book is already in the favorite list and if it exists, else add it to user's favorite books list
        if username in fuser and id in fbook:
            typer.secho(f'Book {id} is already in your favorite list!', fg= typer.colors.RED)    
        else:
            for book in books:
                if book[0] == id:
                    command = f'INSERT INTO fav_books (book_id, username) VALUES (\'{id}\',\'{username}\');'
                    cur.execute(command)
                    typer.secho(f'You added book {id} to your favorites!')
                    break
            else:
                typer.echo(f'Book {id} doesn\'t exist!')
        
    else:
        typer.echo(f"Could not sign in")



def readBooks(user: str):
    '''this function reads a list of books that the user has read'''
    # connect to the database
    params = config('database.ini','CLI_Library')
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    
    # fetch all the books the user has read and return them in a list
    command = f'''SELECT DISTINCT mr.book_id, b.name, a.author_name, b.pages, g.title, 
                CASE
                WHEN inv.book_id IS NULL THEN 'False'
                ELSE 'True'
                END AS availability
                FROM read_books mr
                JOIN books b ON b.id = mr.book_id
                JOIN book_author ab on ab.book_id = b.id
                JOIN author a ON a.id = ab.author_id
                JOIN genre_book gb on gb.book_id = b.id
                join genre g on g.genre_id = gb.genre_id
                LEFT JOIN inventory inv ON inv.book_id = mr.book_id
                WHERE mr.username = '{user}';'''
    cur.execute(command)
    read_books = cur.fetchall()

    return read_books
    
def favoriteBooks(user: str):
    '''This function is called to read the favorite books the user has in their list'''
    # connect to database
    params = config('database.ini','CLI_Library')
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    
    # fetch all the books the user has in their favorite list and return them in a list
    command2 = f'''SELECT DISTINCT fav.book_id, b.name, a.author_name, b.pages, g.title,
            CASE
            WHEN inv.book_id IS NULL THEN 'False'
            ELSE 'True'
            END AS availability
            FROM fav_books fav
            INNER JOIN books b ON b.id = fav.book_id
            RIGHT JOIN book_author ab on ab.book_id = b.id
            LEFT JOIN author a ON a.id = ab.author_id
            right JOIN genre_book gb on gb.book_id = b.id
            left join genre g on g.genre_id = gb.genre_id
            LEFT JOIN inventory inv on inv.book_id = fav.book_id
            WHERE fav.username = '{user}';'''
    
    cur.execute(command2)
    fav_books = cur.fetchall()
    
    return fav_books

def statestics(user: str):
    '''This function is called to show a statistics table of the user's books readings'''
    # connect to the database
    params = config('database.ini','CLI_Library')
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    
    # Fetch all the required information and return them as a list
    command = f'''SELECT COUNT(*) FROM read_books WHERE username = '{user}';,
    SELECT COUNT(ba.author_id) FROM book_author ba
    INNER JOIN read_books rb on rb.book_id = ba.book_id
    WHERE username = '{user}';,
    SELECT COUNT(gb.genre_id) FROM genre_book gb
    INNER JOIN read_books rb on rb.book_id = gb.book_id
    WHERE username = '{user}';,
    SELECT CAST(SUM(b.pages) AS BIGINT) FROM books b
    INNER JOIN read_books rb on rb.book_id = b.id
    WHERE username = '{user}';'''.split(',')
    
    stats = []
    for i in command:
        cur.execute(i)
        stats.append(*cur.fetchall())
    
    return stats
    

def Search_by_name(name : str ) : 
    '''This function is called to allow the user to search for a book by name'''
    try : 
        # connect to database
       params = config('database.ini','CLI_Library')
       conn = psycopg2.connect(**params)
       conn.autocommit = True
       cur = conn.cursor()

        # fetch all information of a book and display them in a table
       cur.execute(f"""SELECT books.id,name,author_name ,pages ,genre.title FROM books 
                       JOIN book_author on books.id = book_author.book_id 
                       JOIN author ON book_author.author_id = author.id 
                       JOIN genre ON books.id = genre.genre_id  
                       WHERE name= \'{name}\' order by name,pages ; """)
       book_names = cur.fetchall()
       # check if the book exists in the inventory, else display the book as not available
       for i in book_names:
            if i[1] == name : 
                table = Table(show_header=True, header_style="bold blue")
                table.add_column("#", style="dim", width=10)
                table.add_column("BookID", style="dim", min_width=10, justify=True)
                table.add_column("Name", style="dim", min_width=10, justify=True)
                table.add_column("Author", style="dim", min_width=10, justify=True)
                table.add_column("Pages", style="dim", min_width=10, justify=True)
                table.add_column("Gener", style="dim", min_width=10, justify=True)
                table.add_column("Availabili__", style="dim", min_width=10, justify=True)    
                table.add_row(f"{i[0]}", f"{i[0]}",f"{i[1]}",f"{i[2]}",f"{i[3]}",f"{i[4]}","True")
                console.print(table)
                break
       else:
         typer.secho(f"the name is wrong", fg=typer.colors.RED)
         raise Exception
            
    except :
             table = Table(show_header=True, header_style="bold blue")
             table.add_column("#", style="dim", width=10)
             table.add_column("BookID", style="dim", min_width=10, justify=True)
             table.add_column("Name", style="dim", min_width=10, justify=True)
             table.add_column("Author", style="dim", min_width=10, justify=True)
             table.add_column("Pages", style="dim", min_width=10, justify=True)
             table.add_column("Gener", style="dim", min_width=10, justify=True)
             table.add_column("Availabili__", style="dim", min_width=10, justify=True)    
             table.add_row("--", "--","--","--","--","--","False")
             console.print(table)
             

def Search_by_author(author : str) : 
    '''This function is called to allow the user to search for a book by author'''
    try : 
        # connect to database
       params = config('database.ini','CLI_Library')
       conn = psycopg2.connect(**params)
       conn.autocommit = True
       cur = conn.cursor()
       cur.execute(f"""SELECT books.id,name ,author_name ,pages ,genre.title FROM books
                        JOIN book_author ON books.id = book_author.book_id 
                        JOIN author ON book_author.author_id = author.id 
                        JOIN genre ON books.id = genre.genre_id 
                        where author_name =\'{author}\'  order by name,pages   ;""")
       aurthor_name = cur.fetchmany()
       # check if the book exists in the inventory, else display the book as not available
       for i in aurthor_name:
         if i[2] == author : 
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("#", style="dim", width=10)
            table.add_column("BookID", style="dim", min_width=10, justify=True)
            table.add_column("Name", style="dim", min_width=10, justify=True)
            table.add_column("Author", style="dim", min_width=10, justify=True)
            table.add_column("Pages", style="dim", min_width=10, justify=True)
            table.add_column("Gener", style="dim", min_width=10, justify=True)
            table.add_column("Availabili__", style="dim", min_width=10, justify=True)    
            table.add_row(f"{i[0]}", f"{i[0]}",f"{i[1]}",f"{i[2]}",f"{i[3]}",f"{i[4]}","True")
            console.print(table)
            break
       else:
            typer.secho(f"the name is wrong", fg=typer.colors.RED)
            raise Exception

    except : 
             table = Table(show_header=True, header_style="bold blue")
             table.add_column("#", style="dim", width=10)
             table.add_column("BookID", style="dim", min_width=10, justify=True)
             table.add_column("Name", style="dim", min_width=10, justify=True)
             table.add_column("Author", style="dim", min_width=10, justify=True)
             table.add_column("Pages", style="dim", min_width=10, justify=True)
             table.add_column("Gener", style="dim", min_width=10, justify=True)
             table.add_column("Availabili__", style="dim", min_width=10, justify=True)    
             table.add_row("--", "--","--","--","--","--","False")
             console.print(table)
        


def Recently_added(GENRE : str):
       
    params = config('database.ini','CLI_Library')
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    
    if GENRE:
        cur.execute(f'''SELECT b.id , b.name ,author_name ,pages ,g.title,
                    CASE
                    WHEN inv.book_id IS NULL THEN 'False'
                    ELSE 'True'
                    END AS availability
                    FROM books b
                    JOIN book_author ON b.id = book_author.book_id 
                    JOIN author ON book_author.author_id = author.id 
                    JOIN genre g ON b.id = g.genre_id  
                    LEFT JOIN inventory inv ON inv.book_id = b.id
                    WHERE inv.last_update = cast('07-04-2023' AS DATE) AND g.title = '{GENRE}'
                    ORDER BY id DESC LIMIT 5;''')
        books = cur.fetchall()
        x = len(books)
        i = 0
        my_result = [i for i in books]
        ii = 0
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("#", style="dim", width=10)
        table.add_column("BookID", style="dim", min_width=10, justify=True)
        table.add_column("Name", style="dim", min_width=10, justify=True)
        table.add_column("Author", style="dim", min_width=10, justify=True)
        table.add_column("Pages", style="dim", min_width=10, justify=True)
        table.add_column("Gener", style="dim", min_width=10, justify=True)
        table.add_column("Availabili__", style="dim", min_width=10, justify=True)
        while ii < x :
            table.add_row(f"{my_result[ii][0]}", f"{my_result[ii][0]}",f"{my_result[ii][1]}",f"{my_result[ii][2]}",f"{my_result[ii][3]}",f"{my_result[ii][4]}",f"{my_result[ii][5]}")
            ii += 1
            console.print(table)
        
    else:
        cur.execute("""SELECT b.id , b.name ,author_name ,pages ,g.title,
                CASE
                WHEN inv.book_id IS NULL THEN 'False'
                ELSE 'True'
                END AS availability
                FROM books b
                JOIN book_author ON b.id = book_author.book_id 
                JOIN author ON book_author.author_id = author.id 
                JOIN genre g ON b.id = g.genre_id  
                LEFT JOIN inventory inv ON inv.book_id = b.id
                WHERE inv.last_update = cast('07-04-2023' AS DATE)
                ORDER BY id DESC LIMIT 5;""")
        books = cur.fetchall()
        x = len(books)
        i = 0
        my_result = [i for i in books]
        ii = 0
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("#", style="dim", width=10)
        table.add_column("BookID", style="dim", min_width=10, justify=True)
        table.add_column("Name", style="dim", min_width=10, justify=True)
        table.add_column("Author", style="dim", min_width=10, justify=True)
        table.add_column("Pages", style="dim", min_width=10, justify=True)
        table.add_column("Gener", style="dim", min_width=10, justify=True)
        table.add_column("Availabili__", style="dim", min_width=10, justify=True)
        while ii < x :
            table.add_row(f"{my_result[ii][0]}", f"{my_result[ii][0]}",f"{my_result[ii][1]}",f"{my_result[ii][2]}",f"{my_result[ii][3]}",f"{my_result[ii][4]}",f"{my_result[ii][5]}")
            ii += 1
            console.print(table)
       
def mostReadBooks(GENRE : str):
    '''This function is called to show the most read books given the genre as an optional argument'''
    # connect to the database
    params = config('database.ini','CLI_Library')
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    
    # if genre argument was given then show most read books according to the genre given, else return most read books
    if GENRE:
        command = f'''SELECT rb.book_id, b.name, a.author_name, g.title, count(rb.book_id) as Number_read
        FROM read_books rb
        JOIN books b ON rb.book_id = b.id
        JOIN book_author ab ON ab.book_id = rb.book_id
        JOIN author a ON a.id = ab.author_id
        JOIN genre_book gb ON gb.book_id = rb.book_id
        JOIN genre g ON g.genre_id = gb.genre_id
        WHERE g.title = '{GENRE}'
        GROUP BY rb.book_id, b.name, a.author_name,g.title
        ORDER BY Number_read DESC
        LIMIT 10;'''
        
        cur.execute(command)
        most_read = cur.fetchall()
        return most_read
    else:
        command = f'''SELECT rb.book_id, b.name, a.author_name, g.title, count(rb.book_id) as Number_read
        FROM read_books rb
        JOIN books b ON rb.book_id = b.id
        JOIN book_author ab ON ab.book_id = rb.book_id
        JOIN author a ON a.id = ab.author_id
        JOIN genre_book gb ON gb.book_id = rb.book_id
        JOIN genre g ON g.genre_id = gb.genre_id
        GROUP BY rb.book_id, b.name, a.author_name,g.title
        ORDER BY Number_read DESC
        LIMIT 10;'''
        
        cur.execute(command)
        most_read = cur.fetchall()
        return most_read

def Most_favorite_books(GENRE : str):
    '''This function is called to show the most favorite books'''
    # connect to database
    params = config('database.ini','CLI_Library')
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    
    # if genre argument was given then show most favorite books according to the genre given, else return most favorite books
    if GENRE:
        command = f'''SELECT fb.book_id, b.name, a.author_name, g.title, count(fb.book_id) as Number_read
        FROM fav_books fb
        JOIN books b ON fb.book_id = b.id
        JOIN book_author ab ON ab.book_id = fb.book_id
        JOIN author a ON a.id = ab.author_id
        JOIN genre_book gb ON gb.book_id = fb.book_id
        JOIN genre g ON g.genre_id = gb.genre_id
        WHERE g.title = '{GENRE}'
        GROUP BY fb.book_id, b.name, a.author_name,g.title
        ORDER BY Number_read DESC
        LIMIT 10;'''
        
        cur.execute(command)
        most_fav = cur.fetchall()
        return most_fav
    else:
        command = f'''SELECT fb.book_id, b.name, a.author_name, g.title, count(fb.book_id) as Number_read
        FROM fav_books fb
        JOIN books b ON fb.book_id = b.id
        JOIN book_author ab ON ab.book_id = fb.book_id
        JOIN author a ON a.id = ab.author_id
        JOIN genre_book gb ON gb.book_id = fb.book_id
        JOIN genre g ON g.genre_id = gb.genre_id
        GROUP BY fb.book_id, b.name, a.author_name,g.title
        ORDER BY Number_read DESC
        LIMIT 10;'''
        
        cur.execute(command)
        most_fav = cur.fetchall()
        return most_fav
    
def mostReadGenres():
    '''This function is called to show the most read genres'''
    # connect to the database
    params = config('database.ini','CLI_Library')
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    
    # fetch most read genres from database and retrun them as a list
    command = f'''SELECT g.title, count(rb.book_id) AS coun FROM genre g
    LEFT JOIN genre_book gb ON gb.genre_id = g.genre_id
    LEFT JOIN read_books rb ON rb.book_id = gb.book_id
    GROUP BY g.title
    ORDER BY coun DESC
    LIMIT 5;'''
    
    cur.execute(command)
    most_genres = cur.fetchall()
    
    return most_genres
    


def Most_read_author():
    '''This function is called to return the most read authors'''
    # connect to the databse
    params = config('database.ini','CLI_Library')
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    
    # fetch all most read authors from the database and return them as a list
    command = f'''
                   SELECT author.author_name, count(rb.book_id) AS coun FROM author
                   LEFT JOIN book_author ON author.id = book_author.author_id
                   LEFT JOIN read_books rb ON rb.book_id = book_author.book_id
                   GROUP BY author_name
                   ORDER BY coun DESC
                   LIMIT 3;  '''
    
    cur.execute(command)
    most_read = cur.fetchall()
    return most_read


if __name__ == '__main__':
    connect()
   