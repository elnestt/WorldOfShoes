from models import get_db_connection, init_db

def seed_products():
    init_db()  # Спочатку ініціалізуємо базу даних
    conn = get_db_connection()
    products = [
        ('Nike Air Force 1',	3475,	'/static/Sneackers/Force.jpg'),
        ('Nike Air Max 1',	3558,	'/static/Sneackers/Airmax.jpg'),
        ('Nike Air Jordan 1',	3959,	'/static/Sneackers/Jordan1.jpg'),
        ('Nike ACG Lowcate',	3009,	'/static/Sneackers/Lowcate.jpg'),
        ('Nike INITIATOR',	3459,	'/static/Sneackers/Initiator.jpg'),
        ('Nike zoom Vomero 5',	3090,	'/static/Sneackers/Vomero.jpg'),
        ('Nike Air Jordan 4',	2446,	'/static/Sneackers/Jordan4.png'),
        ('Nike Air Trainer 1',	4789,	'/static/Sneackers/Trainer.png'),
        ('Nike Jordan Retro 11',	3121,	'/static/Sneackers/Jordan11.jpg'),
        ('Nike Acg Air Mada Low',	3602,	'/static/Sneackers/mada.png'),
        ('Nike Cortez',	4089,	'/static/Sneackers/Cortez.png'),
        ('Nike Air Kukini', 	4500,	'/static/Sneackers/Kukini.png'),
    ]
    
    conn.executemany('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', products)
    conn.commit()#Зберігаємо зміни
    conn.close()

if __name__ == '__main__':
    seed_products()
    print("Тестові продукти додано до бази даних.")