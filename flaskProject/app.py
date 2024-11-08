from flask import Flask, render_template, Blueprint
from routes.admin import admin_bp
from models import init_db

app = Flask(__name__)

init_db()


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

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')



if __name__ == '__main__':
    app.run(debug=True)
