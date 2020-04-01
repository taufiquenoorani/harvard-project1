# Project 1

## Index.html
As soon as the user logs in, they will be displayed with the home page. Home page has search bar that will allow user to search for books by title, author or ISBN. User can use partial keywords to display all matching results.

## Account.html
This page displays user account information (username, first name, and last name)

## Books.html
This page provides the list of books matching user's query at the home page. If the query is invalid, or if the book cannot be found in the database, the page will display with an error. Successful query result will display title, book name, author name, and year. Users will have an option to click on `details` link to show more details about that specific book.

## Layout.html
Layout is the template page that populates navigation bar, and header to each page.

## Login.html
Users will have to provide username and password to login. Incorrect credentials will display an error.

## Register.html
Users will be able to register with a unique username, password, first name and last name.

## Search.html
This page will display details about a specific book. The result displays goodreads total ratings, average ratings, user ratings and comments.

## 404.html
If user browse to an incorrect URL, they will be displayed with a custom 404 error.

## import.csv
This script will allow user to import books.csv to database set with "DATABASE_URL" environmental variable.

## /SQL/books.sql
[books.sql](https://github.com/taufique786/project1-taufique786/blob/master/SQL/books.sql) contains the database structure for table books
```
CREATE TABLE books (
  isbn VARCHAR (255) PRIMARY KEY,
  title VARCHAR (255) NOT  NULL,
  author VARCHAR (255) NOT NULL,
  year  VARCHAR(4)  NOT NULL
);
```

## /SQL/reviews.sql
[reviews.sql](https://github.com/taufique786/project1-taufique786/blob/master/SQL/reviews.sql) contains the database structure for table reviews
```
CREATE TABLE reviews (
  user_id INT NOT NULL,
  isbn  VARCHAR(10) NOT NULL,
  rate  INT NOT  NULL,
  comment TEXT NOT NULL
);
```

## /SQL/users.sql
[users.sql](https://github.com/taufique786/project1-taufique786/blob/master/SQL/users.sql) contains the database structure for table users
```
CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR (255) UNIQUE NOT NULL,
  password VARCHAR (255) NOT NULL,
  firstname VARCHAR (255) NOT NULL,
  lastname VARCHAR (255) NOT NULL
);
```

## application.py
This file is the main logic behind this project. The file contains routes to all pages and how to handle user requests when they come in.
