from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from config import DB_CONFIG
from ml.predict import predict_price

app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        hashed = generate_password_hash(request.form['password'])
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (request.form['name'], request.form['email'], hashed)
        )
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s",
                       (request.form['email'],))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], request.form['password']):
            session['user'] = user['name']
            return redirect('/')
    return render_template("login.html")

@app.route('/search')
def search():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.*, a.airline_name
        FROM flights f
        JOIN airlines a ON f.airline_id=a.airline_id
    """
    )
    flights = cursor.fetchall()
    conn.close()

    for f in flights:
        f['predicted_price'] = predict_price(10, f['stops'], f['airline_id'])

    return render_template("results.html", flights=flights)

@app.route('/admin')
def admin_dashboard():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT airline_name, COUNT(*) as total
        FROM flights
        JOIN airlines USING(airline_id)
        GROUP BY airline_name
        ORDER BY total DESC
        LIMIT 3
    """)
    data = cursor.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", data=data)

if __name__ == "__main__":
    app.run()