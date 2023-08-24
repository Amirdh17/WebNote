from flask import redirect, render_template, session
from functools import wraps
import sqlite3 as sql

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def checkValidPass(s):
    ''' checking the length of password that should > 8 and should include atleast one integer and one character '''
    n = len(s)
    if n < 8:
        return False
    if (any(chr.isdigit() for chr in s) == False):
        return False
    if (any(c.isalpha() for c in s) == False):
        return False
    return True

# To remember the logged in user details
def remember_login(state):
    session["name"] = session.get("name")
    session["user_id"] = session.get("user_id")
    #if state:
    session["state"] = state

# Get database connection
def get_db_connection():
    conn = sql.connect('webnote.db')
    conn.row_factory = sql.Row
    return conn

def getJulianday():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT julianday('now','localtime') AS d")
    dt = cur.fetchall()
    con.close()
    return dt[0]['d']