from flask import Blueprint, render_template, request, redirect, url_for, session
from models import get_products, add_order

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    products = get_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart = session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {'id': product_id, 'name': product['name'], 'price': product['price'], 'quantity': 1}
        session['cart'] = cart
    return redirect(url_for('catalog.catalog'))

@catalog_bp.route('/cart')
def cart():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@catalog_bp.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    email = request.form['email']
    address = request.form['address']
    add_order(email, address, cart)
    session['cart'] = {}
    return redirect(url_for('catalog.catalog'))

@catalog_bp.route('/catalog')
def catalog():
    # Отримуємо параметри сторінки та ліміту з URL (за замовчуванням page=1, limit=5)
    page = int(request.args.get('page', 1))  
    limit = int(request.args.get('limit', 5))

    # Отримуємо список усіх товарів.
    all_products = get_products() 
    total_products = len(all_products)

    total_pages = (total_products + limit - 1) // limit

    start = (page - 1) * limit  # Індекс першого товару 
    end = start + limit  # Індекс останнього товару 

    products = all_products[start:end]  # Створюємо підмножину товарів для сторінки.

    return render_template(
        'catalog.html',  # Шаблон HTML, який буде використовуватися для рендерингу.
        products=products, 
        page=page,  
        limit=limit,
        total_pages=total_pages, 
        total_products=total_products  
    )





