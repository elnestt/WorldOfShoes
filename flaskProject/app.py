from flask import Flask, render_template, jsonify, request
from routes.admin import admin_bp
from routes.catalog import catalog_bp
from routes.feedback import feedback_bp
from routes.login import login_bp
from routes.api import api_bp
from models import init_db
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Додаємо секретний ключ

# Функція для завантаження даних з JSON
def load_products():
    with open('products.json', 'r') as file:  # Вказуємо шлях до вашого JSON-файлу
        return json.load(file)

# Функція для пошуку кросівок за назвою
def get_shoes_by_name(name):
    products = load_products()  # Завантажуємо дані з JSON
    return [product for product in products if name.lower() in product['name'].lower()]  # Фільтруємо дані

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

init_db() 
app.register_blueprint(feedback_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(login_bp)
app.register_blueprint(api_bp)



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

