from flask import Flask, render_template, request, redirect, url_for, session, flash
from routes.admin import admin_bp
from routes.catalog import catalog_bp
from routes.feedback import feedback_bp
from routes.login import login_bp
from models import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Додаємо секретний ключ

init_db() 
app.register_blueprint(feedback_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(login_bp)


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


if __name__ == '__main__':
    app.run(debug=True)
