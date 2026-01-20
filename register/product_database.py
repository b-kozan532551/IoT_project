import sqlite3

class Product:
    def __init__(self, id: int, value: int):
        self.id = id
        self.value = value
        

def _get_cursor():
    connection = sqlite3.connect('product_data.db')
    return connection.cursor()

def initialize_product_db():
    cursor = _get_cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            cost INTEGER NOT NULL
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM products WHERE id = ?', (5900197032608,))

    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO products (id, cost) VALUES (?, ?)', (5900197032608, 10000))

    cursor.connection.commit()
    cursor.connection.close()

def get_product(id: int) -> Product:
    cursor = _get_cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    result = cursor.fetchone()
    cursor.connection.close()

    if result:
        return Product(id=result[0], value=result[1])
    return None