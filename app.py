from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            description TEXT NOT NULL
                          )''')
        conn.commit()

# Initialize the database
init_db()

# Homepage route
@app.route('/')
def homepage():
    return render_template('homepage.html')

# Contact Page route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        description = request.form['description']

        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO contacts (name, age, email, description) VALUES (?, ?, ?, ?)',
                               (name, age, email, description))
                conn.commit()
            return redirect(url_for('homepage'))
        except sqlite3.IntegrityError:
            return "Email already exists. Please use a different email."

    return render_template('contact.html')

# Fetch Description Page route
@app.route('/fetch', methods=['GET', 'POST'])
def fetch():
    description = None
    if request.method == 'POST':
        email = request.form['email']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT description FROM contacts WHERE email = ?', (email,))
            result = cursor.fetchone()
            if result:
                description = result[0]
            else:
                description = "No description found for the provided email."

    return render_template('fetch.html', description=description)

if __name__ == '__main__':
    app.run(debug=True)
