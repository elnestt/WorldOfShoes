
from flask import Flask, render_template, Blueprint, session
from routes.admin import admin_bp
from models import init_db
from routes.catalog import catalog_bp
from routes.feedback import feedback_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Додаємо секретний ключ

init_db() 
app.register_blueprint(feedback_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(admin_bp)


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

@app.route('/shop')
def shop():
    return render_template('shop.html')


if __name__ == '__main__':
    app.run(debug=True)
