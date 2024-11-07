from models import get_db_connection, init_db

def seed_products():
    init_db()  # Спочатку ініціалізуємо базу даних
    conn = get_db_connection()
    products = [
        ('Nike Air Force 1',	3475,	'/api/placeholder/200/200'),
        ('Nike Air Max 1',	3558,	'/api/placeholder/200/200'),
        ('Nike Air Jordan 1',	3959,	'/api/placeholder/200/200'),
        ('Nike ACG Lowcate',	3009,	'/api/placeholder/200/200'),
        ('Nike INITIATOR',	3459,	'/api/placeholder/200/200'),
        ('Nike Air Max Dawn',	3090,	'/api/placeholder/200/200'),
        ('Nike Air Jordan 4',	2446,	'/api/placeholder/200/200'),
        ('Nike Air Trainer 1',	4789,	'/api/placeholder/200/200'),
        ('Nike Jordan Retro 11',	3121,	'/api/placeholder/200/200'),
        ('Nike Acg Air Mada Low',	3602,	'/api/placeholder/200/200'),
        ('Nike Cortez',	4089,	'/api/placeholder/200/200'),
        ('Nike Air Kukini', 	4500,	'/api/placeholder/200/200'),
    ]
    
    conn.executemany('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', products)
    conn.commit()#Зберігаємо зміни
    conn.close()

if __name__ == '__main__':
    seed_products()
    print("Тестові продукти додано до бази даних.")