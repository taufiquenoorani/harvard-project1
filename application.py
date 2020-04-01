import os
import requests
from flask import Flask, session, render_template, request, flash , redirect,url_for, jsonify
from flask_session import Session
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=['GET','POST'])
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('index.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.route("/register", methods=['POST', 'GET'])
def register():
    if session.get('logged_in'):
        return redirect (url_for('index'))

    else:
        if request.method == "POST":
            # Create User Profile
            username = request.form.get("username")
            password = request.form.get("password")
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")

            # Generate Password Hash
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

            # Check if username already exists
            if db.execute("SELECT * FROM users WHERE username=:username LIMIT 1", {"username": username}).rowcount != 0:
                flash('Username already taken!', 'danger')
                return redirect (url_for('register'))

            else:
                # Create User Profile in PSQL
                db.execute("INSERT INTO users (username, password, firstname, lastname) VALUES(:username, :password, :firstname, :lastname)",{"username": username, "password": password_hash, "firstname": firstname, "lastname": lastname})

                # Commit Changes
                db.commit()
                flash('Account successfully created!', 'success')

                # Redirect User to Login Page
                return redirect (url_for('login'))
    return render_template('register.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if session.get('logged_in'):
        return redirect (url_for('index'))

    else:
        if request.method == "POST":
            # Grab username and password
            username = request.form.get("username")
            password = request.form.get("password")

            session['user'] = username

            # Fetch username from PSQL
            user = db.execute("SELECT user_id, password FROM users WHERE username=:username", {"username": username}).fetchone()

            # Verify if user is authenticated
            if db.execute("SELECT * FROM users WHERE username=:username", {'username':username}).rowcount==0 or bcrypt.check_password_hash(user.password, password) == False:
                flash('Please check your username and password and try again', 'danger')
            else:
                session['logged_in'] = True
                return redirect (url_for('index'))
    return render_template("login.html")


@app.route("/logout")
def logout():
    # Remove user from session
    session.pop('logged_in', None)
    session['user'] = []
    return redirect (url_for('login'))


@app.route("/account")
def account():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # Get user information from database
        user_account = db.execute("SELECT username, firstname, lastname FROM users WHERE username=:username", {'username':session['user']})
        return render_template("account.html", user_account=user_account)


@app.route("/books", methods=['GET','POST'])
def books():
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        search = request.form.get("search")

        # Check if search is null, redirect to homepage
        if search is "":
            return redirect (url_for('index'))

        else:
            # Adding wildcard to previous variable
            query = '%' + search + '%'

            # Search for books in database
            books = db.execute("SELECT * FROM books WHERE author ILIKE :query OR title ILIKE :query OR isbn ILIKE :query", {"query": query}).fetchall()

            # Count number of books
            total_books = len(books)

            # Check if the user is logged out
            if not session.get('logged_in'):
                return redirect (url_for('login'))
            return render_template("books.html", books=books, total_books=total_books)


@app.route("/search/<string:bookisbn>", methods=['GET', 'POST'])
def search(bookisbn):
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        books = db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn': bookisbn}).fetchone()

        # Get Current User ID
        user_id = db.execute("SELECT user_id FROM users WHERE username=:username", {"username": session["user"]}).fetchone()[0]

        # Total Reviews
        total_reviews = db.execute("SELECT COUNT(rate) FROM reviews WHERE isbn = :isbn", {"isbn": bookisbn}).fetchone()[0]

        # Average Reviews
        avg_ratings = db.execute("SELECT AVG(rate) FROM reviews WHERE isbn = :isbn", {"isbn": bookisbn}).fetchone()[0]

        # Get GoodReaders Reviews
        good_reads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "oCYNGrqPgZeOJa3OS065Q", "isbns": bookisbn})

        # Parsing good_reads into JSON format
        good_reads_json = good_reads.json()['books'][0]

        good_reads_avg = good_reads_json['average_rating']
        good_reads_total = good_reads_json['ratings_count']

        # Display user Reviews
        user_reviews = db.execute("SELECT username, comment, rate FROM users FULL OUTER JOIN reviews ON users.user_id = reviews.user_id WHERE isbn = :isbn", {"isbn": bookisbn})

        if request.method == "POST":
            # Get User Rating
            rating = request.form.get('options')

            # Get User Comment
            comment = request.form.get('comment')

            # Check if user has already submitted a review
            if db.execute("SELECT * FROM reviews WHERE (user_id = :user_id) AND (isbn = :isbn)", {"user_id": user_id, "isbn": bookisbn}).rowcount > 0:
                flash("You have already reviewed this book!", 'warning')

            else:
                # Submit Review to SQL
                db.execute("INSERT INTO reviews (user_id, isbn, rate, comment) VALUES (:user_id, :isbn, :rate, :comment)", {"user_id": user_id, "isbn": bookisbn, "rate": rating, "comment": comment})

                # Commit Changes
                db.commit()

                flash("Thank you for submitting your review!", 'success')

        return render_template("search.html", books=books, total_reviews=total_reviews, avg_ratings=avg_ratings, good_reads_avg=good_reads_avg, good_reads_total=good_reads_total, user_reviews=user_reviews)


@app.route("/api/<string:bookisbn>")
def api(bookisbn):
    books = db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn': bookisbn}).fetchone()

    # Show 404 if ISBN isn't available in the database
    if books is None:
        return jsonify({"error": "404 Book Not Found"})
    else:
        # Get the average ratings from reviews table
        review_count = db.execute("SELECT COUNT(rate) FROM reviews WHERE isbn = :isbn", {"isbn": bookisbn}).fetchone()[0]

    # Return the data user has requested
    return jsonify({
        "title": books[1],
        "author": books[2],
        "year": books[0],
        "isbn": books[3],
        "review_count": str(review_count)
        })
