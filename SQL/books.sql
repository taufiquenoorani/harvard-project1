-- d78ro601fa780v=> \d+ books;
--                                            Table "public.books"
--  Column |          Type          | Collation | Nullable | Default | Storage  | Stats target | Description
-- --------+------------------------+-----------+----------+---------+----------+--------------+-------------
--  isbn   | character varying(255) |           | not null |         | extended |              |
--  title  | character varying(255) |           | not null |         | extended |              |
--  author | character varying(255) |           | not null |         | extended |              |
--  year   | character varying(4)   |           | not null |         | extended |              |
-- Indexes:
--     "books_pkey" PRIMARY KEY, btree (isbn)

CREATE TABLE books (
  isbn VARCHAR (255) PRIMARY KEY,
  title VARCHAR (255) NOT  NULL,
  author VARCHAR (255) NOT NULL,
  year  VARCHAR(4)  NOT NULL
);
