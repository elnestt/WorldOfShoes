from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from routes.admin import admin_bp
from routes.catalog import catalog_bp
from routes.feedback import feedback_bp
from routes.login import login_bp
from routes.api import api_bp
from models import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Додаємо секретний ключ

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

def create_response(data=None, message="", status="success", code=200):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    }), code

@app.route('/api/data', methods=['POST'])
def handle_json_data():
    data = request.get_json()
    if not data or 'name' not in data:
        return create_response(message="Invalid or missing JSON data", status="error", code=400)

    name = data['name']
    return create_response(data={"greeting": f"Hello, {name}!"}, message="Request successful")

@app.route('/api/response', methods=['GET'])
def json_response():
    return create_response(data={"info": "This is a JSON response"})

if __name__ == '__main__':
    app.run(debug=True)

