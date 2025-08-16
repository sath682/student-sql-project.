from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS students
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   roll TEXT UNIQUE NOT NULL,
                   marks INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        marks = request.form['marks']
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, roll, marks) VALUES (?, ?, ?)", 
                    (name, roll, marks))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/result', methods=['GET', 'POST'])
def view_result():
    student = None
    if request.method == 'POST':
        roll = request.form['roll']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE roll=?", (roll,))
        student = cur.fetchone()
        conn.close()
    return render_template('view_result.html', student=student)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
