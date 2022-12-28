# all the imports
from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = './tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


# before each request, connect to the database
@app.before_request
def before_request():
    g.db = connect_db()

# after each request, close the database
@app.teardown_request
def teardown_request(exception):
    g.db.close()

# connect to the database and return a connection object        
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# create the database if it doesn't exist yet
def init_db():
    with closing(connect_db()) as db: # db is a connection object.
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read().decode('utf-8')) 
            # The executescript method executes all the SQL statements in the string.
        db.commit()

"""
This is the main page of the application. It shows all the entries in the database.
"""
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    # cur is a cursor object. It has a fetchall method that returns a list of tuples.
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    
    return render_template('show_entries.html', entries=entries)


# This is the login page. It uses the session object to store the logged in state.
@app.route('/add', methods=['POST'])
def add_entry():
    
    if not session.get('logged_in'):
        abort(401)
    # The request object is used to get the data from the form.
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None # The error message is stored in this variable. It is passed to the template.
    if request.method == 'POST': # If the user has submitted the form.
        if request.form['username'] != app.config['USERNAME']: # If the user has submitted the wrong username.
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']: # If the user has submitted the wrong password.
            error = 'Invalid password'
        else: # If the user has entered the correct username and password.
            session['logged_in'] = True # Set the logged_in flag in the session object.
            flash('You were logged in') # Send a flash message to the user.
            return redirect(url_for('show_entries')) # Return to the main page.
    return render_template('login.html', error=error)

# This is the logout page. It uses the session object to remove the logged in state.
@app.route('/logout')
def logout():
    session.pop('logged_in', None) # Remove the logged_in flag from the session object.
    flash('You were logged out') # Send a flash message to the user and redirect to the home page.
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()

