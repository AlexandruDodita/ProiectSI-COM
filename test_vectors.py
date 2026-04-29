from aes_crypto import AESCrypto

def test_aes_basic():
    print("test 1: criptare si decriptare baza")
    aes = AESCrypto(b'cheie_test_12345' + b'\x00' * 16)

    plaintext = "mesaj secret de test"
    encrypted = aes.encrypt(plaintext)
    decrypted = aes.decrypt(encrypted)

    print(f"  text original: {plaintext}")
    print(f"  text criptat: {encrypted[:50]}...")
    print(f"  text decriptat: {decrypted}")
    print(f"  succes: {plaintext == decrypted}\n")

def test_aes_empty():
    print("test 2: mesaj gol")
    aes = AESCrypto(b'alta_cheie_test1' + b'\x00' * 16)

    plaintext = ""
    encrypted = aes.encrypt(plaintext)
    decrypted = aes.decrypt(encrypted)

    print(f"  text original: '{plaintext}'")
    print(f"  text decriptat: '{decrypted}'")
    print(f"  succes: {plaintext == decrypted}\n")

def test_aes_long():
    print("test 3: mesaj lung")
    aes = AESCrypto(b'cheie_lunga_test' + b'\x00' * 16)

    plaintext = "acesta este un mesaj foarte lung care contine multe caractere si va fi impartit in mai multe blocuri aes pentru a testa functionalitatea de padding si unpadding a algoritmului de criptare simetrica implementat"
    encrypted = aes.encrypt(plaintext)
    decrypted = aes.decrypt(encrypted)

    print(f"  lungime text: {len(plaintext)} caractere")
    print(f"  lungime criptat: {len(encrypted)} caractere")
    print(f"  succes: {plaintext == decrypted}\n")

def test_aes_unicode():
    print("test 4: caractere unicode")
    aes = AESCrypto(b'cheie_unicode123' + b'\x00' * 16)

    plaintext = "mesaj cu caractere speciale: ăâîșț àéè 你好"
    encrypted = aes.encrypt(plaintext)
    decrypted = aes.decrypt(encrypted)

    print(f"  text original: {plaintext}")
    print(f"  text decriptat: {decrypted}")
    print(f"  succes: {plaintext == decrypted}\n")

def test_aes_binary():
    print("test 5: date binare")
    aes = AESCrypto(b'cheie_binara_123' + b'\x00' * 16)

    plaintext = bytes([i for i in range(256)])
    encrypted = aes.encrypt(plaintext)
    decrypted_bytes = aes.decrypt(encrypted).encode('latin1')

    print(f"  lungime date binare: {len(plaintext)} bytes")
    print(f"  succes: {plaintext == decrypted_bytes}\n")

if __name__ == "__main__":
    print("=== vectori de test pentru aes ===\n")
    test_aes_basic()
    test_aes_empty()
    test_aes_long()
    test_aes_unicode()
    print("toate testele au fost executate")
