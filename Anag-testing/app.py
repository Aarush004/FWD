from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Connect to the SQLite database
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Retrieve all users from the database
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()

    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']

    # Connect to the SQLite database
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Insert new user into the database
    c.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
