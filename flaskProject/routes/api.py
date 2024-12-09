from flask import Blueprint, jsonify, request,session
from models import (
    get_users,
    get_products,
    get_orders,
    get_order_details,
    add_order,
    update_order_status,
    delete_order,
    get_user_by_id,
    register_user,
    login_user,
    get_db_connection,
    add_feedback,
    login_user,
    register_user
)
api_bp = Blueprint('api', __name__)

#Get all products
@api_bp.route('/api/products', methods=['GET'])
def get_products_api():
    # Перевірка, чи користувач авторизований
    if 'user_id' not in session:
        return jsonify({
            "status": "error",
            "message": "You must be logged in to access this resource."
        }), 401  # Повертаємо код помилки 401 (Unauthorized)
    
    # Перевірка, чи користувач є адміністратором
    if not session.get('is_admin', False):  # Перевірка на admin права
        return jsonify({
            "status": "error",
            "message": "You do not have admin rights."
        }), 403  # Повертаємо код помилки 403 (Forbidden)

    try:
        # Отримуємо товари
        products = get_products()
        return jsonify([dict(product) for product in products]), 200  # Повертаємо список продуктів та статус 200 (OK)
    except Exception as e:
        # Якщо сталася помилка, повертаємо повідомлення про помилку
        return jsonify({'error': str(e)}), 500  # Повертаємо код помилки 500 (Internal Server Error)

    

#Get all orders
@api_bp.route('/api/orders', methods=['GET'])
def get_orders_api():
    if 'user_id' not in session:
        return jsonify({
            "status": "error",
            "message": "You must be logged in to access this resource."
        }), 401
    if session.get('is_admin') is not True:  # Перевірка, чи є користувач адміністратором
        return jsonify({
            "status": "error",
            "message": "You do not have admin rights."
        }), 403
    try:
        orders = get_orders()
        return jsonify([dict(order) for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500  
    
#Get order details
@api_bp.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order_details_api(order_id):
    if 'user_id' not in session:
        return jsonify({
            "status": "error",
            "message": "You must be logged in to access this resource."
        }), 401
    if session.get('is_admin') is not True:  # Перевірка, чи є користувач адміністратором
        return jsonify({
            "status": "error",
            "message": "You do not have admin rights."
        }), 403
    try:
        order, items = get_order_details(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify({
            'order': dict(order),
            'items': [dict(item) for item in items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

#Add order
@api_bp.route('/api/orders', methods=['POST'])
def add_order_api():
    if 'user_id' not in session:
        return jsonify({
            "status": "error",
            "message": "You must be logged in to access this resource."
        }), 401
    if session.get('is_admin') is not True:  # Перевірка, чи є користувач адміністратором
        return jsonify({
            "status": "error",
            "message": "You do not have admin rights."
        }), 403
    try:
        data = request.get_json()
        email = data.get('email')
        address = data.get('address')
        cart = data.get('cart')

        if not email or not address or not cart:
            return jsonify({'error': 'Missing email, address, or cart'}), 400

        add_order(email, address, cart)
        return jsonify({'message': 'Order added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#Delete order
@api_bp.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order_api(order_id):
    if 'user_id' not in session:
        return jsonify({
            "status": "error",
            "message": "You must be logged in to access this resource."
        }), 401
    if session.get('is_admin') is not True:  # Перевірка, чи є користувач адміністратором
        return jsonify({
            "status": "error",
            "message": "You do not have admin rights."
        }), 403
    try:
        delete_order(order_id)
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#Get all users
@api_bp.route('/api/users', methods=['GET'])
def get_all_users():
    if 'user_id' not in session:
        return jsonify({
            "status": "error",
            "message": "You must be logged in to access this resource."
        }), 401
    if session.get('is_admin') is not True:  # Перевірка, чи є користувач адміністратором
        return jsonify({
            "status": "error",
            "message": "You do not have admin rights."
        }), 403
    try:
        users = get_users()
        return jsonify([dict(user) for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
    
#Get user by id
@api_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id_api(user_id):
    if 'user_id' not in session:
        return jsonify({
            "status": "error",
            "message": "You must be logged in to access this resource."
        }), 401
    if session.get('is_admin') is not True:  # Перевірка, чи є користувач адміністратором
        return jsonify({
            "status": "error",
            "message": "You do not have admin rights."
        }), 403
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(dict(user)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Register user
@api_bp.route('/api/register', methods=['POST'])
def register_user_api():
    if 'user_id' not in session:
        return jsonify({
            "status": "error",
            "message": "You must be logged in to access this resource."
        }), 401
    if session.get('is_admin') is not True:  # Перевірка, чи є користувач адміністратором
        return jsonify({
            "status": "error",
            "message": "You do not have admin rights."
        }), 403
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'error': 'Missing username, email, or password'}), 400

        result = register_user(username, email, password)
        return jsonify({'message': result}), 201 if "успішна" in result else 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#Login user
@api_bp.route('/api/login', methods=['POST'])
def login_user_api():
    if 'user_id' not in session:
        return jsonify({
            "status": "error",
            "message": "You must be logged in to access this resource."
        }), 401
    if session.get('is_admin') is not True:  # Перевірка, чи є користувач адміністратором
        return jsonify({
            "status": "error",
            "message": "You do not have admin rights."
        }), 403
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        user = login_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['email'] = user['email']
            return jsonify({'message': 'Login successful', 'user': {'id': user['id'], 'email': user['email']}}), 200

        return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#Admin delete feedback
@api_bp.route('/api/admin/delete_feedback/<int:id>', methods=['DELETE'])
def admin_delete_feedback(id):
    if session.get('is_admin', False):
        return jsonify({'error': 'У вас немає прав адміна'}), 403
    
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM feedback WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Відгук успішно видалено!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#Admin order
@api_bp.route('/api/admin/orders/<int:id>', methods=['GET'])
def admin_get_order_details(id):
    if session.get('is_admin', False):
        return jsonify({'error': 'У вас немає прав адміна'}), 403
    try:
        order, items = get_order_details(id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify({
            'order': dict(order),
            'items': [dict(item) for item in items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 


#Admin update order
@api_bp.route('/api/admin/update_order_status/<int:id>', methods=['PUT'])
def admin_update_order_status(id):
    if session.get('is_admin', False):  # Перевірка, чи є в сесії ключ is_admin
        return jsonify({'error': 'У вас немає прав адміна'}), 403

    try:
        # Отримуємо новий статус із JSON тіла запиту
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({'error': 'Не вказано статус замовлення'}), 400
        
        # Оновлюємо статус замовлення в базі даних
        update_order_status(id, status)
        
        return jsonify({'message': 'Статус замовлення оновлено успішно'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#Admin delete order
@api_bp.route('/api/admin/delete_order/<int:id>', methods=['DELETE'])
def admin_delete_order_api(id):
    if session.get('is_admin', False):
        return jsonify({'error': 'У вас немає прав адміна'}), 403
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM orders WHERE id = ?', (id,))
        conn.commit()
        conn.close()
    
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Add contact
@api_bp.route('/api/contacts', methods=['POST'])
def add_feedback_api():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Перевірка обов'язкових полів
        if not name or not email or not message:
            return jsonify({'error': 'Missing name, email, or message'}), 400

        # Збереження контакту у таблицю feedback
        add_feedback(name, email, message)

        return jsonify({'message': 'Message added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



