import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

with open('books.csv', 'r') as books:
    read_books = csv.reader(books)

    # Skip the header
    next(read_books)

    for isbn, title, author, year in read_books:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES(:isbn, :title, :author, :year)",{"isbn": isbn, "title": title, "author": author, "year": year})
        db.commit()
