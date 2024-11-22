from flask import Blueprint, jsonify, request, json
from models import (
    get_db_connection,
    get_users,
    get_products,
    get_orders,
    get_order_details,
    add_order,
    update_order_status,
    delete_order
)
api_bp = Blueprint('api', __name__)

# Products endpoints
@api_bp.route('/api/products', methods=['GET'])
def get_all_products():
    try:
        products = get_products()
        return jsonify([dict(product) for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    



def get_shoes_by_name(name):
    conn = get_db_connection()  # Підключення до БД
    query = "SELECT * FROM products WHERE LOWER(name) LIKE ?"  # Запит до бази
    rows = conn.execute(query, (f'%{name.lower()}%',)).fetchall()  # Виконання запиту
    conn.close()  # Закриття з'єднання
    return rows

# Ендпоінт для пошуку товарів
@api_bp.route('/api/products/search', methods=['POST'])
def search_shoes():
    name = request.form.get('name')  # Отримуємо значення поля "name"

    if not name:  # Якщо поле відсутнє або порожнє
        return jsonify({
            "status": "error",
            "message": "The 'name' field is required",
            "data": None
        }), 400

    shoes = get_shoes_by_name(name)  # Виклик функції пошуку

    if not shoes:
        return jsonify({
            "status": "error",
            "message": f"No shoes found with name '{name}'",
            "data": None
        }), 404

    return jsonify({
        "status": "success",
        "message": "Shoes found successfully",
        "data": [dict(row) for row in shoes]
    }), 200



# Orders endpoints
@api_bp.route('/api/order', methods=['GET'])
def get_all_orders():
    try:
        orders = get_orders()
        return jsonify([dict(order) for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
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

@api_bp.route('/api/order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'address' not in data or 'cart' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        add_order(data['email'], data['address'], data['cart'])
        return jsonify({'message': 'Order created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@api_bp.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):

    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        update_order_status(order_id, data['status'])
        return jsonify({'message': 'Order updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/order/<int:order_id>', methods=['DELETE'])
def remove_order(order_id):
    try:
        delete_order(order_id)
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Feedback endpoints
@api_bp.route('/api/contacts', methods=['GET'])
def get_all_feedback():
    try:
        conn = get_db_connection()
        feedback = conn.execute('SELECT * FROM feedback').fetchall()
        conn.close()
        return jsonify([dict(f) for f in feedback]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/contacts', methods=['POST'])
def create_feedback():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['name', 'email', 'message']):
            return jsonify({'error': 'All fields are required'}), 400
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)',
            (data['name'], data['email'], data['message'])
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Feedback submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/contacts/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    """
    Видалення одного відгуку за ID
    """
    try:
        conn = get_db_connection()
        # Перевіряємо чи існує відгук
        feedback = conn.execute('SELECT * FROM feedback WHERE id = ?', (feedback_id,)).fetchone()
        
        if not feedback:
            return jsonify({'error': 'Feedback not found'}), 404
            
        conn.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Feedback deleted successfully',
            'deleted_id': feedback_id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
# Users endpoints
@api_bp.route('/api/users', methods=['GET'])
def get_all_users():
    try:
        users = get_users()
        return jsonify([dict(user) for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
