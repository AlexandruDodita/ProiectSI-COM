from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

class AESCrypto:
    def __init__(self, key=None):
        # genereaza cheie de 256 biti sau foloseste cea furnizata
        if key is None:
            self.key = get_random_bytes(32)
        else:
            self.key = key if len(key) == 32 else pad(key.encode() if isinstance(key, str) else key, 32)[:32]

    def encrypt(self, plaintext):
        # cripteaza textul folosind aes in modul cbc
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')

        cipher = AES.new(self.key, AES.MODE_CBC)
        iv = cipher.iv
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        return base64.b64encode(iv + ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        # decripteaza textul
        data = base64.b64decode(ciphertext)
        iv = data[:16]
        ciphertext_bytes = data[16:]

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext_bytes), AES.block_size)

        return plaintext.decode('utf-8')

    def get_key(self):
        return self.key
