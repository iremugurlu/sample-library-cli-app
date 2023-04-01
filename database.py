import psycopg2
import typer
from rich.console import Console
from rich.table import Table

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
            break
    else:
        typer.secho(f"username or password is wrong!", fg=typer.colors.RED)
        
            
    
if __name__ == '__main__':
    connect()




if __name__ == '__main__':
    connect()


