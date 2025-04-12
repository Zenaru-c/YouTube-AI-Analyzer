# ##[*.importing modules]
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
import sqlite3
from youtube_ai import analyze_youtube_comments
from dotenv import load_dotenv
from datetime import datetime, timedelta
import bcrypt

# ##[*.loading env variable]
load_dotenv()

# ##[*.static session setup]
app = Flask(__name__, static_folder='static')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ##[*."secret" key for flash messages]
app.secret_key = "elonmeluskhuskofemluosok"

# ##[*.database setup]
DATABASE = "users.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                failed_attempts INTEGER DEFAULT 0,
                lock_time TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)
        conn.commit()


init_db()

# ##[*.web routes]
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["login-username"].strip()
        password = request.form["login-password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
                cursor.execute("""
                    INSERT INTO logins (user_id)
                    VALUES (?)
                """, (user["id"],))
                conn.commit()

                cursor.execute("""
                    UPDATE users
                    SET last_login = CURRENT_TIMESTAMP,
                        failed_attempts = 0
                    WHERE id = ?
                """, (user["id"],))
                conn.commit()

                session["user_id"] = user["id"]
                session["username"] = user["username"]
                flash("Login successful!", "success")
                return redirect(url_for("welcome"))
            else:
                cursor.execute("""
                    UPDATE users
                    SET failed_attempts = failed_attempts + 1
                    WHERE id = ?
                """, (user["id"],))
                conn.commit()

                flash("Invalid credentials. Please try again.", "danger")
        else:
            flash("Something isn't right. Try again!", "danger")

    return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["register-username"].strip()
        password = request.form["register-password"]
        confirm_password = request.form["re-enter-password"]

        if not username or not password or password != confirm_password:
            flash("Please fill out all fields and make sure the passwords match", "danger")
            return redirect(url_for("register"))

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            flash("Username already taken. Try a different one.", "danger")
            return redirect(url_for("register"))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        flash("Registration succesful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    session.pop("username", None)

    flash("You have been logged out", "info")

    return redirect(url_for("login"))


@app.route("/welcome")
def welcome():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT created_at, last_login
        FROM users
        WHERE id = ?
    """, (session["user_id"],))
    user_data = cursor.fetchone()

    return render_template("welcome.html",
                         created_at=user_data["created_at"],
                         last_login=user_data["last_login"])


@app.route("/artificial_intelligence", methods=["GET", "POST"])
def artificial_intelligence():
    if "user_id" not in session:
        return redirect(url_for("login"))

    ai_response = None
    if request.method == "POST":
        youtube_url = request.form["youtube_url"]
        ai_response = analyze_youtube_comments(youtube_url)
        ai_response = ai_response.strip().replace("\n", " ")

    return render_template("artificial_intelligence.html", ai_response=ai_response, now=datetime.now().strftime("%H:%M:%S"))

@app.route("/settings")
def settings():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT login_time
        FROM logins
        WHERE user_id = ?
        ORDER BY login_time DESC
        LIMIT 10
    """, (session["user_id"],))
    login_history = cursor.fetchall()

    cursor.execute("""
        SELECT created_at
        FROM users
        WHERE id = ?
    """, (session["user_id"],))
    user_data = cursor.fetchone()

    created_at = user_data["created_at"] if user_data else None

    return render_template("settings.html",
                           login_history=login_history,
                           username=session["username"],
                           created_at=created_at)

@app.route("/security")
def security():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("security.html")

@app.route("/delete_account", methods=["POST"])
def delete_account():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM logins WHERE user_id = ?
    """, (session["user_id"],))

    cursor.execute("""
        DELETE FROM users WHERE id = ?
    """, (session["user_id"],))

    conn.commit()

    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


