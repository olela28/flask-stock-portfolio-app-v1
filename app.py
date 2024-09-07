from cs50 import SQL # type: ignore
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session # type: ignore
from werkzeug.security import check_password_hash, generate_password_hash

from templates.helpers import login_required, usd, lookup, apology

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

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 403)
        stock = lookup(request.form.get("symbol"))
        if stock is None: 
            return apology("Invalid stock")
        shares = request.form.get("shares")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide valid number of shares")
        
        user_id = session["user_id"]

        rows = db.execute(
            "SELECT cash FROM users WHERE id = ?", user_id
        )

        cash = rows[0]["cash"]

        total_cost = stock["price"] * int(shares)

        if cash < total_cost:
            return apology("Insufficient funds for this purchase")
        
        db.execute(
            "UPDATE users SET cash = cash - ?", total_cost, user_id
        )

        db. execute("""
            INSERT INTO transactions (user_id, symbol, shares, price, total, transaction_type)
            VALUES(?,?,?,?,?)""",
                   user_id, symbol, int(shares), stock["price"], total_cost, "BOUGHT"
        )
        flash("Bought!")
        return redirect("/")
    return render_template("buy.html")

@app.route("/history", methods=["GET","POST"])
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("""
                              SELECT symbol, price, shares, total, transaction_time, transaction_type
                              FROM transactions
                              WHERE user_id = ?
                              ORDER BY transaction_time DESC""",
                              user_id)
    return render_template("history.html", transactions=transactions)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )
        
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)
        
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")
        
        quote = lookup(symbol)
        if quote is None:
            return apology("Invalid symbol")
        
        price = usd(quote["price"])
        return render_template("quoted.html", quote=quote, price=price)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user in database"""

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if not request.form.get("password"):
            return apology("must provide password", 400)
        if not request.form.get("confirmation"):
            return apology("must reenter password", 400)
        
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match!")
        
        try:
            rows = db.execute(
                "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )
        except Exception as e:
            return apology("Error!")
        if len(rows) == 1:
            return apology("Username already exists!", 400)
        
        hash = generate_password_hash(request.form.get("password"))
        
        rows = db.execute(
                          "INSERT INTO users (username, hash) VALUES(?,?)",
                          request.form.get("username"), hash)
        
        return redirect("/")
    return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session["user_id"]    

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")
        
        shares_to_sell = request.form.get("shares")
        if not shares_to_sell or not shares_to_sell.isdigit() or int(shares_to_sell) <= 0:
            return apology("must provide valid number of shares")
        
        shares_to_sell = int(shares_to_sell)

        rows = db.execute("""
                          SELECT SUM(shares) AS total_shares
                          FROM transactions
                          WHERE user_id = ?
                          AND symbol = ?
                          GROUP BY symbol
                          HAVING SUM(shares) > 0""",
                          user_id, symbol)

        if len(rows) != 1 or rows[0]["total_shares"] > shares_to_sell:
            return apology("Input exceeds number of shares in your portfolio")
        
        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid stock")
        
        sale = stock["price"] * shares_to_sell

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale, user_id)

        db.excecute("""
                    INSERT INTO transactions (user_id, symbol, shares, price, total, transaction_type)
                    VALUES(?, ?, ?, ?, ?,?)""",
                    user_id, symbol, shares_to_sell, stock["price"], sale, "SOLD")
        
        flash("Sold!")
        return redirect("/")
    
    symbols = db.execute("""
                             SELECT symbol, SUM(shares) AS total_shares
                             FROM transactions
                             WHERE user_id = ?
                             GROUP BY symbol
                             HAVING SUM(shares) > 0""",
                             user_id)
    return render_template("sell.html", symbols=symbols)