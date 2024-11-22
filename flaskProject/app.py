<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
=======
from flask import Flask, render_template, jsonify, request
>>>>>>> 7e4cc29f7a9e9ea0c61c7023c9e4a8c33538a36d
from routes.admin import admin_bp
from routes.catalog import catalog_bp
from routes.feedback import feedback_bp
from routes.login import login_bp
from routes.api import api_bp
from models import init_db
import json
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Додаємо секретний ключ

init_db() 
app.register_blueprint(feedback_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(login_bp)
app.register_blueprint(api_bp)

# Функція для підключення до бази даних SQLite
def get_db_connection():
    conn = sqlite3.connect('flaskProject/db world of shoes.db')  # Замініть на назву вашої бази даних
    conn.row_factory = sqlite3.Row  # Це дозволяє повертати дані як словники
    return conn

def get_shoes_by_name(name):
    conn = get_db_connection()  # Викликаємо функцію для створення з'єднання
    query = "SELECT * FROM products WHERE LOWER(name) LIKE ?"  # Запит для пошуку товарів
    rows = conn.execute(query, (f'%{name.lower()}%',)).fetchall()  # Виконання запиту
    conn.close()  # Закриття з'єднання

# Ендпоінт для пошуку кросівок
@app.route('/api/products', methods=['POST'])
def search_shoes():
    data = request.get_json()  # Отримуємо JSON-запит
    if not data or 'name' not in data:
        return jsonify({
            "status": "error",
            "message": "The 'name' field is required",
            "data": None
        }), 400

    name = data['name']
    shoes = get_shoes_by_name(name)

    if not shoes:
        return jsonify({
            "status": "error",
            "message": f"No shoes found with name '{name}'",
            "data": None
        }), 404

    return jsonify({
        "status": "success",
        "message": "Shoes found successfully",
        "data": shoes
    }), 200

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/catalog2')
def catalog2():
    return render_template('catalog2.html')

@app.route('/location')
def location():
    return render_template('location.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found, sorry"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request, sorry"}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error, sorry"}), 500

if __name__ == '__main__':
    app.run(debug=True)

