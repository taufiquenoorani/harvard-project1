-- d78ro601fa780v=> \d+ users;
--                                                             Table "public.users"
--   Column   |          Type          | Collation | Nullable |                Default                 | Storage  | Stats target | Description
-- -----------+------------------------+-----------+----------+----------------------------------------+----------+--------------+-------------
--  user_id   | integer                |           | not null | nextval('users_user_id_seq'::regclass) | plain    |              |
--  username  | character varying(255) |           | not null |                                        | extended |              |
--  password  | character varying(255) |           | not null |                                        | extended |              |
--  firstname | character varying(255) |           | not null |                                        | extended |              |
--  lastname  | character varying(255) |           | not null |                                        | extended |              |
-- Indexes:
--     "users_pkey" PRIMARY KEY, btree (user_id)
--     "users_username_key" UNIQUE CONSTRAINT, btree (username)

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR (255) UNIQUE NOT NULL,
  password VARCHAR (255) NOT NULL,
  firstname VARCHAR (255) NOT NULL,
  lastname VARCHAR (255) NOT NULL
);
