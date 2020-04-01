-- d78ro601fa780v=> \d+ reviews;
--                                           Table "public.reviews"
--  Column  |         Type          | Collation | Nullable | Default | Storage  | Stats target | Description
-- ---------+-----------------------+-----------+----------+---------+----------+--------------+-------------
--  user_id | integer               |           | not null |         | plain    |              |
--  isbn    | character varying(10) |           | not null |         | extended |              |
--  rate    | integer               |           | not null |         | plain    |              |
--  comment | text                  |           | not null |         | extended |              |

CREATE TABLE reviews (
  user_id INT NOT NULL,
  isbn  VARCHAR(10) NOT NULL,
  rate  INT NOT  NULL,
  comment TEXT NOT NULL
);
