from cryptography.fernet import Fernet


def decrypt_data_by_key_with_fernet(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


def encrypt_data_by_key_with_fernet(data: str, key: bytes = None):
    """
    Шифрует переданную строку случайным ключом.
    Возвращает словарь с двумя ключами 'cipher' и 'key', где 'cipher'
    является результатом шифрования, а 'key' ключом для расшифровки
    сообщения. """
    if not key:
        key = Fernet.generate_key()
    ciphertext = Fernet(key).encrypt(data.encode())

    return {'cipher': ciphertext, 'key': key}
