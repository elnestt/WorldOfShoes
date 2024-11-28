import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


def get_db_connection():
    conn = sqlite3.connect('WorldOfShoes/flaskProject/db world of shoes.db')
    conn.row_factory = sqlite3.Row
    return conn

#Ініціалізація бази даних
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, message TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, image TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, address TEXT, total_price REAL, status TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS order_items (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, product_id INTEGER, quantity INTEGER, FOREIGN KEY (order_id) REFERENCES orders (id), FOREIGN KEY (product_id) REFERENCES products (id))')
    conn.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL, password INTEGER NOT NULL UNIQUE, is_admin INTEGER)')

    conn.commit()
    conn.close()

#Отримати товари
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return products

#Додати замовлення
def add_order(email, address, cart):
    conn = get_db_connection()
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    cur = conn.cursor()
    cur.execute('INSERT INTO orders (email, address, total_price, status, date) VALUES (?, ?, ?, ?, ?)',
                (email, address, total_price, 'Нове замолення', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    order_id = cur.lastrowid
    for item in cart.values():
        cur.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)',
                    (order_id, item['id'], item['quantity']))
    conn.commit()
    conn.close()

#Отримати всі замовлення
def get_orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return orders

#Отримати деталі замовлення
def get_order_details(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    items = conn.execute('SELECT oi.quantity, p.name, p.price FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE oi.order_id = ?', (order_id,)).fetchall()
    conn.close()
    return order, items

#Оновлення статусу замовлення
def update_order_status(order_id, status):
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()

#Видалення замовлення
def delete_order(order_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM order_items WHERE order_id = ?', (order_id,))
    conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()

#Реєстрація користувача
def register_user(username, email, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
    if user:
        conn.close()
        return "Користувач з таким ім'ям або email вже існує."
    
    #Хешування паролю
    hashed_password = generate_password_hash(password)
    conn.execute('INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)', (username, email, hashed_password, 0))
    conn.commit()
    conn.close()
    return "Реєстрація успішна! Тепер ви можете увійти."

# Функція входу користувача
def login_user(email, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        return user
    return None

# Функція для отримання інформації про користувача за ID
def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

# Функція для отримання даних про користувачів
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return users

def add_feedback(id, name, email, message=None):
    try:
        # Підключення до бази даних
        conn = sqlite3.connect('flaskProject/db world of shoes.db')  # Змініть на ваш файл бази даних
        cursor = conn.cursor()
        
 
        # SQL-запит для вставки відгуку
        query = """
        INSERT INTO feedback (name, email, message)
        VALUES (?, ?, ?)
        """
        
        # Виконання запиту
        cursor.execute(query, (name, email, message))
        conn.commit()
        
        # Закриття курсора і з'єднання
        cursor.close()
        conn.close()
        print("Feedback added successfully!")
    except sqlite3.Error as e:
        # Обробка помилок SQLite
        print(f"Database error: {e}")
        raise
    except Exception as e:
        # Інші помилки
        print(f"Unexpected error: {e}")
        raise