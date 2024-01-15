from pathlib import os
from cryptography.fernet import Fernet, InvalidToken

def encrypt_or_decrypt(data, encrypt=True):
    try:
        key = os.getenv('KEY').encode('utf-8')
        cipher_suite = Fernet(key)

        if isinstance(data, memoryview):
            data = data.tobytes()
        
        if not isinstance(data, bytes):
            data = data.encode('utf-8')

        if encrypt:
            text = cipher_suite.encrypt(data)
        else:
            text = cipher_suite.decrypt(data).decode('utf-8')
        
        return text

    except Exception as e:
        # Lidar com o erro aqui, por exemplo, imprimir uma mensagem de log
        print(f"Erro durante a operação de {'criptografia' if encrypt else 'descriptografia'}: {e}")
        return ""