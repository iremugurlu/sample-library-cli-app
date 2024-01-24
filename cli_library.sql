CREATE TABLE "user" (
	"username" varchar(255) NOT NULL,
	"password" int NOT NULL,
	CONSTRAINT "user_pk" PRIMARY KEY ("username")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "books" (
	"id" serial NOT NULL,
	"name" varchar(255) NOT NULL,
	"pages" bigint NOT NULL,
	CONSTRAINT "books_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "author" (
	"id" serial NOT NULL,
	"author_name" varchar(255) NOT NULL,
	CONSTRAINT "author_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "book_author" (
	"book_id" bigint NOT NULL,
	"author_id" bigint NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "genre" (
	"genre_id" serial NOT NULL,
	"title" TEXT NOT NULL,
	CONSTRAINT "genre_pk" PRIMARY KEY ("genre_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "genre_book" (
	"book_id" bigint NOT NULL,
	"genre_id" bigint NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "borrowed_books" (
	"bb_id" serial NOT NULL,
	"book_id" bigint NOT NULL,
	"username" varchar(255) NOT NULL,
	CONSTRAINT "borrowed_books_pk" PRIMARY KEY ("bb_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "inventory" (
    "inventory_id" serial NOT NULL,
	"book_id" bigint NOT NULL,
	"last_update" DATE NOT NULL,
    CONSTRAINT "inventory_pk" PRIMARY KEY ("inventory_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "fav_books" (
	"fav_id" serial NOT NULL,
	"book_id" bigint NOT NULL,
	"username" varchar(255) NOT NULL,
	CONSTRAINT "fav_books_pk" PRIMARY KEY ("fav_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "read_books" (
	"mark_id" serial NOT NULL,
	"username" varchar(255) NOT NULL,
	"book_id" bigint NOT NULL,
	CONSTRAINT "read_books_pk" PRIMARY KEY ("mark_id")
) WITH (
  OIDS=FALSE
);






ALTER TABLE "book_author" ADD CONSTRAINT "book_author_fk0" FOREIGN KEY ("book_id") REFERENCES "books"("id");
ALTER TABLE "book_author" ADD CONSTRAINT "book_author_fk1" FOREIGN KEY ("author_id") REFERENCES "author"("id");


ALTER TABLE "genre_book" ADD CONSTRAINT "genre_book_fk0" FOREIGN KEY ("book_id") REFERENCES "books"("id");
ALTER TABLE "genre_book" ADD CONSTRAINT "genre_book_fk1" FOREIGN KEY ("genre_id") REFERENCES "genre"("genre_id");

ALTER TABLE "borrowed_books" ADD CONSTRAINT "borrowed_books_fk0" FOREIGN KEY ("book_id") REFERENCES "books"("id");
ALTER TABLE "borrowed_books" ADD CONSTRAINT "borrowed_books_fk1" FOREIGN KEY ("username") REFERENCES "user"("username");

ALTER TABLE "inventory" ADD CONSTRAINT "inventory_fk0" FOREIGN KEY ("book_id") REFERENCES "books"("id");

ALTER TABLE "fav_books" ADD CONSTRAINT "fav_books_fk0" FOREIGN KEY ("book_id") REFERENCES "books"("id");
ALTER TABLE "fav_books" ADD CONSTRAINT "fav_books_fk1" FOREIGN KEY ("username") REFERENCES "user"("username");

ALTER TABLE "read_books" ADD CONSTRAINT "read_books_fk0" FOREIGN KEY ("username") REFERENCES "user"("username");
ALTER TABLE "read_books" ADD CONSTRAINT "read_books_fk1" FOREIGN KEY ("book_id") REFERENCES "books"("id");


INSERT INTO "user" (username, password) VALUES ('john2', '12345');
INSERT INTO "user" (username, password) VALUES ('jbiever1', '4568');
INSERT INTO "user" (username, password) VALUES ('sthomazet2', '7891');













