import psycopg2

def create_tables():
	""" create tables in the PostgreSQL database"""
	commands = (
		"""
 		
		CREATE TABLE IF NOT EXISTS public.books
(
    book_id serial NOT NULL ,
    title character varying(100) COLLATE pg_catalog."default" NOT NULL,
    author character varying(100) COLLATE pg_catalog."default",
    genre character varying(100) COLLATE pg_catalog."default",
    pages integer,
    added_date date DEFAULT CURRENT_DATE,
    quantity integer NOT NULL,
    CONSTRAINT books_pkey PRIMARY KEY (book_id),
    CONSTRAINT uk_books UNIQUE (title, author)
)
		""",
		""" CREATE TABLE IF NOT EXISTS public.user_action
(
    action_id serial NOT NULL,
    user_id integer NOT NULL,
    book_id integer NOT NULL,
    borrow boolean DEFAULT false,
    reading boolean DEFAULT false,
    read boolean DEFAULT false,
    fav boolean DEFAULT false,
    will_read boolean DEFAULT false,
    CONSTRAINT pk_action_id PRIMARY KEY (action_id)
)
		""",
 		"""CREATE TABLE IF NOT EXISTS public.users
(
    user_id serial NOT NULL,
    user_name character varying(100) NOT NULL,
    CONSTRAINT pk_user_id PRIMARY KEY (user_id),
    CONSTRAINT uk_user_name UNIQUE (user_name)
)
  """,
  		"""ALTER TABLE IF EXISTS public.user_action
    ADD CONSTRAINT fk_books_actions FOREIGN KEY (book_id)
    REFERENCES public.books (book_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;""",
	"""ALTER TABLE IF EXISTS public.user_action
    ADD FOREIGN KEY (user_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
 
	"""
  )
	conn = psycopg2.connect(
	host="localhost",
	database="library",
	user="postgres",
	password="postgres")
	try:
		cur = conn.cursor()
		for command in commands:
			cur.execute(command)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

if __name__ == '__main__':
	create_tables()
