from flask import Flask, render_template,session
from models import init_db
from routes.catalog import catalog_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Додаємо секретний ключ

init_db() 

app.register_blueprint(catalog_bp)

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

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
