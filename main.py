from flask import Flask, flash, redirect, render_template, request, session
import sqlite3 as sql
from flask_session import Session
from helper import login_required, checkValidPass, remember_login, get_db_connection, getJulianday
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    ''' index page where user can add and edit notes '''
    # check if user logged in
    if not session.get("name"):
        return redirect("/login")

    # display the appropriate message
    if session.get("state"):
        flash(session["state"])
        session.pop("state")

    if request.method == "POST":
        heading = request.form.get("head")
        noting = request.form.get("notes")
        # check whether the user entered All fields
        if not heading or not noting:
            remember_login("Fill all coulumns")
            return redirect("/")

        id = session.get("user_id")
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT julianday('now','localtime') AS d")
        dt = cur.fetchall()
        con.close()
        try:
            with sql.connect("webnote.db") as con:
                con = get_db_connection()
                cur = con.cursor()
                cur.execute("INSERT INTO notes (user_id, heading, noted, dateandtime) VALUES (?, ?, ?, ?)", [id, heading, noting, dt[0]['d']])
                con.commit()
                con.close()
        except:
            remember_login("Notes Not saved!")
            return redirect("/")

        # Remember which user has logged in
        print("success")
        remember_login("Notes have successfully saved!")

        # All good, go to index page
        return redirect("/")


    else:
        return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    ''' LogIn '''
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # ensure username and password are given
        if not username or not password:
            state = "should provide both username and password"
            return render_template("login.html", data=state)
        # Check whether the user name is valid or not
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("select * from users where username = ?", [username])
        rows = cur.fetchall()
        con.close()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("login.html", data="Username or password is invalid!")
        # Remember which user has logged in
        session["name"] = username
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["POST", "GET"])
def register():
    ''' Register the user '''
    if request.method == "POST":

        try:
            # get user entered values
            username = request.form.get("username")
            pass1 = request.form.get("password")
            pass2 = request.form.get("password1")
            # check all fields have entered
            if not username or not pass1 or not pass2:
                return render_template("register.html", data="Enter All Fields")
            else:
                if (pass1 != pass2):
                    return render_template("register.html", data="Password mismatch")
            # validate password
            if (checkValidPass(pass1) == False):
                return render_template("register.html", data="Password should have length more than 8 and should include atleast 1 number and 1 alphabet")

            # Generate hash for the password
            pass1 = generate_password_hash(pass1)

            with sql.connect("webnote.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, hash) VALUES (?,?)", [username, pass1])
                con.commit()
        except:
            msg = "error in insert operation. Use different user name"
            return render_template("register.html",data = msg)

        con = get_db_connection()
        cur = con.cursor()
        cur.execute("select id from users where username = ?", [username])
        rows = cur.fetchall()
        con.close()

        # Remember which user has logged in
        session["name"] = username
        session["user_id"] = rows[0]["id"]
        session["state"] = "Registered!"
        # All good, go to index page
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/view", methods=["POST", "GET"])
@login_required
def view():
    ''' to view the notes and edit them '''
    # display the appropriate message
    if session.get("state"):
        flash(session["state"])
        session.pop("state")

    id = session.get("user_id")
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("select note_id, heading, noted, date(dateandtime) AS dt, time(dateandtime) AS tm from notes where user_id = ?", [id])
    rows = cur.fetchall()
    con.close()

    if request.method == "POST":
        action = request.form.get('action')
        if action == 'update':
            note_id = request.form.get('note_id')
            call_head = f'head{note_id}'
            heading = request.form.get(call_head)
            call_note = f'notes{note_id}'
            notes = request.form.get(call_note)
            print(note_id)
            dt = getJulianday()

            with sql.connect("webnote.db") as con:
                con = get_db_connection()
                cur = con.cursor()
                cur.execute("UPDATE notes SET heading = ?, noted = ?, dateandtime = ? WHERE note_id = ?", [heading, notes, dt, note_id])
                con.commit()
                con.close()

        else:
            note_id = request.form.get('note_id')
            con = get_db_connection()
            cur = con.cursor()
            cur.execute("DELETE FROM notes WHERE note_id = ?", [note_id])
            con.commit()
            con.close()

        con = get_db_connection()
        cur = con.cursor()
        cur.execute("select note_id, heading, noted, date(dateandtime) AS dt, time(dateandtime) AS tm from notes where user_id = ?", [id])
        rows = cur.fetchall()
        con.close()

        return render_template("view.html", data=rows)

    else:
        return render_template("view.html", data=rows)

