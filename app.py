from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)



import sqlite3

def init_db():
    conn = sqlite3.connect('bills.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            fuel_type TEXT,
            rate REAL,
            liters REAL,
            total_amount REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fuel_type = request.form['fuel_type']
        rate = float(request.form['rate'])
        liters = float(request.form['liters'])
        total_amount = rate * liters
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to database
        conn = sqlite3.connect('bills.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bills (date, fuel_type, rate, liters, total_amount) VALUES (?, ?, ?, ?, ?)',
                       (date, fuel_type, rate, liters, total_amount))
        conn.commit()
        conn.close()

        return render_template('index.html', total=total_amount)

    return render_template('index.html', total=None)

@app.route('/history')
def history():
    conn = sqlite3.connect('bills.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bills ORDER BY id DESC')
    all_bills = cursor.fetchall()
    conn.close()
    return render_template('history.html', bills=all_bills)

if __name__ == '__main__':
    app.run(debug=False, port=10000)
