import sqlite3
from logger_config import log
from hash_data import hash_data_and_check


def get_cursor():
    connection = sqlite3.connect('payment_data.db')
    return connection.cursor()


def create_db():
    cursor = get_cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS card_data (
            id TEXT PRIMARY KEY,
            pin TEXT NOT NULL,
            email TEXT,
            balance INTEGER NOT NULL
        )
    ''')
    cursor.connection.commit()


def add_card_info(id, pin, email=None, balance=0):
    cursor = get_cursor()

    log.info(f'Inserting card {id} to the database')
    try:
        cursor.execute('INSERT INTO card_data (id, pin, email, balance) VALUES (?, ?, ?, ?)', (id, pin, email, balance))
        cursor.connection.commit()
        log.info('Card data inserted successfully.')
    except sqlite3.IntegrityError:
        log.info('Failed to add card data.')


def get_card_data(id):
    cursor = get_cursor()

    log.info(f'Searching data for card with id: {id}')
    cursor.execute('SELECT * FROM card_data WHERE id = ?', (id,))
    result = cursor.fetchone()

    if result:
        log.info('Fetching card data')
        return {'id': result[0], 'pin': result[1], 'email': result[2], 'balance': result[3]}
    else:
        log.info('No card in the database matches this id')
        return None


def update_card_balance(id, new_balance):
    cursor = get_cursor()

    log.info(f'Updating balance for card with id: {id} to {new_balance}')
    cursor.execute('UPDATE card_data SET balance = ? WHERE id = ?', (new_balance, id))

    if cursor.rowcount > 0:
        cursor.connection.commit()
        log.info('Balance updated successfully')
        return True
    else:
        log.info('No card in the database matches this id')
        return False
