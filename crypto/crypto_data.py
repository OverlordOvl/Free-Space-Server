from __future__ import annotations
from cryptography.fernet import Fernet
from typing import List, Union


def decrypt_data_by_key_with_fernet(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


def encrypt_data_by_key_with_fernet(data: str, key: Union[str, bytes] = None) -> List[bytes]:
    """
    Шифрует переданную строку случайным ключом.
    Возвращает словарь с двумя ключами 'cipher' и 'key', где 'cipher'
    является результатом шифрования, а 'key' ключом для расшифровки
    сообщения. """
    if not key:
        key = Fernet.generate_key()
    if type(key) == str:
        key = key.encode('utf-8')
    ciphertext = Fernet(key).encrypt(data.encode())

    return [ciphertext, key]
