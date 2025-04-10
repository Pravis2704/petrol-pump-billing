from flask import Flask, render_template, request
import datetime
import sqlite3

app = Flask(__name__)

fuel_prices = {
    "Petrol": 110.0,
    "Diesel": 95.0,
    "CNG": 80.0
}

# --- DB SETUP ---
def init_db():
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        fuel TEXT,
        quantity REAL,
        rate REAL,
        total REAL,
        date TEXT
    )''')
    conn.commit()
    conn.close()

def save_bill_to_db(name, fuel_type, quantity, rate, total, date):
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()
    c.execute("INSERT INTO bills (name, fuel, quantity, rate, total, date) VALUES (?, ?, ?, ?, ?, ?)",
              (name, fuel_type, quantity, rate, total, date))
    conn.commit()
    conn.close()

# --- ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def home():
    bill = ""
    if request.method == 'POST':
        name = request.form['name']
        fuel_type = request.form['fuel']
        quantity = float(request.form['quantity'])

        rate = fuel_prices[fuel_type]
        total = quantity * rate
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        bill = f"""===== PETROL PUMP BILL =====
Date: {now}
Customer Name: {name}
Fuel Type: {fuel_type}
Rate per Litre: ₹{rate}
Quantity: {quantity} L
----------------------------
Total Amount: ₹{total}
============================
Thank You! Drive Safe!
"""

        save_bill_to_db(name, fuel_type, quantity, rate, total, now)

    return render_template('index.html', bill=bill, fuel_prices=fuel_prices)

# --- INIT DB + SERVER ---
if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=10000)
