from cs50 import SQL # type: ignore
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session # type: ignore
from werkzeug.security import check_password_hash, generate_password_hash

from templates.helpers import login_required, usd, lookup

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"]= "filesystem"
Session(app)

# Configure cs50 library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached!"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]

    rows = db.execute("""
                      SELECT cash, symbol,
                      SUM(shares) AS total_shares
                      FROM users
                      LEFT JOIN transactions ON users.id = transactions.user_id
                      WHERE users.id = ?
                      GROUP BY symbol
                      HAVING total_shares > 0 OR symbol is NULL""",
                      user_id)
    
    cash = rows[0]["cash"] if rows else 0

    results = []
    stock_value = 0

    for row in rows:
        if row["symbol"] is None:
            continue

        stock = lookup(row["symbol"])
        if stock:
            row["price"] = stock["price"]
            row["total"] = row["total_shares"] * row["price"]
            stock_value += row["total"]
            results.append(row)

    grand_total = cash + stock_value

    return render_template("index.html", cash=cash, results=results, stock_value=stock_value, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""



@app.route("/history", methods=["GET","POST"])
@login_required
def history():
    """Show history of transactions"""



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""


@app.route("/logout")
def logout():
    """Log user out"""


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote"""


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    """Register user in database"""


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""