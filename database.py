import psycopg2
import typer
from rich.console import Console
from rich.table import Table
import datetime

from config import config


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
            conn.autocommit = True 
            curr = conn.cursor()
                
            curr.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            table_names = curr.fetchall()
            
            if len(table_names) != 0:
                typer.echo("Database tables are already created!")
                typer.echo("Existing tables:")
                for table in table_names:
                    curr.execute(f'SELECT * FROM {table[0]};')  
                    typer.echo(table)
                    typer.echo(curr.fetchall())
                    
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
        
            # curr.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            # table_names = curr.fetchall()
            # for table in table_names:
            #     # cur.execute(f'SELECT * FROM {table[0]};')  
            #     print(table)
            #     print(cur.fetchall())
            
            # print(len(curr.fetchall()), ' tables created.')
            # cur.execute('SELECT * FROM students;')
            # print(cur.fetchall())
            # cur.execute('SELECT * from teachers;')
            # print(cur.fetchall())
            # curr.close()
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    
    
                  
    finally: 
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    
def connect_to_db():
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
            print(error)
            
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)      

def singUp(username: str, password: int):
    params = config('database.ini','CLI_Library')
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('SELECT username FROM public."user";')
    
    user = cur.fetchall()
    for i in user:
        if username == i[0]:
            typer.secho(f"This user already exist! Try different user", fg=typer.colors.RED)
            break
    else:   
        command = f'INSERT INTO "user" (username, password) VALUES (\'{username}\',\'{password}\');'
        cur.execute(command)
        cur.close()

def signIn(username: str, password: int):
    try:
        params = config('database.ini','CLI_Library')
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute('SELECT username FROM public."user";')
        user = cur.fetchall()
        cur.execute('SELECT password FROM public."user";')
        user_pass = cur.fetchall()
        
        for i,j in zip(user, user_pass):
            if username == i[0] and password == j[0]:
                typer.secho(f"You are signed in", fg=typer.colors.GREEN)
                success = True
                break
                
        else:
            typer.secho(f"username or password is wrong!", fg=typer.colors.RED)
            success = False
        
        return success
    except ValueError:
        print('Please Enter valid information')

def addBook(bookname: str, author: str, pages: int, genre: str):    
    try:
        try:
            params = config('database.ini','CLI_Library')
            conn = psycopg2.connect(**params)
            conn.autocommit = True
            cur = conn.cursor()
            
            command_query = f''' SELECT name FROM books;
            SELECT author_name FROM author;'''.split('\n')
            
            queried_data = []
            for i in command_query:
                cur.execute(i)
                queried_data.append(cur.fetchall())
            
            
            
            
            
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
                print('hello')
                commandd = f'''INSERT INTO "books" (name,pages) VALUES (\'{bookname}\',\'{pages}\');
                INSERT INTO "author" (author_name) VALUES (\'{author}\');
                INSERT INTO "book_author" (book_id, author_id) VALUES ((SELECT id FROM "books" WHERE name = \'{bookname}\'), (SELECT id FROM "author" WHERE author_name = \'{author}\'));
                INSERT INTO "inventory" (book_id, last_update) VALUES ((SELECT id FROM "books" WHERE name = \'{bookname}'), \'{datetime.date.today()}\');'''
                cur.execute(commandd)
            
            command = f'SELECT title FROM genre;'
            cur.execute(command)
            genre_title = cur.fetchall()
            
            
            for title in genre_title:
                if title[0] == genre:
                    command = f'INSERT INTO "genre_book" (book_id, genre_id) VALUES ((SELECT id FROM "books" WHERE name = \'{bookname}\'), (SELECT genre_id FROM "genre" WHERE title = \'{genre}\'));'
                    cur.execute(command)
                    break

            else:
                cur.execute(f'INSERT INTO "genre" (title) VALUES (\'{genre}\');')
            
        except psycopg2.DatabaseError as e:
            print(e)
            
        
    except (SyntaxError, ValueError, psycopg2.DatabaseError) as e:
        typer.echo(f"Could not sign in", e)
   
                    
        
        
            
    
if __name__ == '__main__':
    connect()