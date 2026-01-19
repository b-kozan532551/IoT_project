import hashlib


def hash_data(id, pin):
    return hashlib.sha256((id + pin).encode()).hexdigest()


def hash_data_and_check(id, pin, received_data):
    data_hash = hash_data(id, pin)
    return data_hash == received_data
