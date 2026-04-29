import threading
import time
from secure_station import SecureStation

def test_simple_communication():
    print("=== test 1: comunicare simpla ===\n")

    # callback pentru mesajele primite de statia 2
    received_messages = []
    def on_message(msg):
        received_messages.append(msg)

    # porneste statia 2 (server)
    station2 = SecureStation(5002, "statia2")
    server_thread = threading.Thread(target=station2.start_server, args=(on_message,))
    server_thread.daemon = True
    server_thread.start()

    time.sleep(1)

    # statia 1 trimite mesaj
    station1 = SecureStation(5001, "statia1")
    message = "mesaj secret de test"
    station1.connect_and_send(5002, message)

    time.sleep(2)

    print(f"\ntest finalizat: mesaj trimis = '{message}'")
    print(f"rezultat: {'succes' if message in received_messages else 'esuat'}\n")

def test_long_message():
    print("=== test 2: mesaj lung (multiple blocuri) ===\n")

    received_messages = []
    def on_message(msg):
        received_messages.append(msg)

    station2 = SecureStation(5004, "statia2")
    server_thread = threading.Thread(target=station2.start_server, args=(on_message,))
    server_thread.daemon = True
    server_thread.start()

    time.sleep(1)

    station1 = SecureStation(5003, "statia1")
    message = "acesta este un mesaj foarte lung care va fi impartit in mai multe blocuri pentru a testa functionalitatea de fragmentare si reasamblare a mesajelor criptate " * 10
    station1.connect_and_send(5004, message)

    time.sleep(3)

    print(f"\ntest finalizat: lungime mesaj = {len(message)} caractere")
    print(f"rezultat: {'succes' if message in received_messages else 'esuat'}\n")

def test_bidirectional():
    print("=== test 3: comunicare bidirectionala ===\n")

    print("test pentru comunicare bidirectionala")
    print("statia 1 -> statia 2: mesaj de la prima statie")
    print("apoi statia 2 -> statia 1: raspuns de la a doua statie")
    print("(necesita rulare manuala cu doua procese separate)\n")

if __name__ == "__main__":
    print("=== teste pentru comunicarea criptata ===\n")

    try:
        test_simple_communication()
        time.sleep(1)
        test_long_message()
        time.sleep(1)
        test_bidirectional()

    except KeyboardInterrupt:
        print("\nteste oprite")
    except Exception as e:
        print(f"\neroare: {e}")
