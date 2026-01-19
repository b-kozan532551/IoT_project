from database_config import update_card_balance, get_card_data
from hash_data import hash_data_and_check
from logger_config import log


def check_balance(data, value):
    if data['balance'] >= value:
        update_card_balance(data['id'], data['balance'] - value)
        return True

    return False


def verify_payment(id, data_hash, value):
    log.info('Veryfying the payment')
    data = get_card_data(id)

    if data is None:
        log.error()
        return False

    if hash_data_and_check(data['id'], data['pin'], data_hash):
        if check_balance(data, value):
            return True

    return False