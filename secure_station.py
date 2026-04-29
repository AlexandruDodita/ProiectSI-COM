import socket
import json
import threading
from aes_crypto import AESCrypto
from key_agreement import DiffieHellman
from message_splitter import MessageSplitter

class SecureStation:
    def __init__(self, port, station_name="station"):
        self.port = port
        self.station_name = station_name
        self.aes = None
        self.dh = DiffieHellman()
        self.splitter = MessageSplitter(block_size=512)
        self.received_blocks = []

    def start_server(self, callback=None):
        # porneste serverul pentru a asculta conexiuni
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', self.port))
        server.listen(1)

        print(f"[{self.station_name}] server pornit pe portul {self.port}")

        conn, addr = server.accept()
        print(f"[{self.station_name}] conexiune de la {addr}")

        # schimb de chei diffie-hellman
        self._key_exchange_server(conn)

        # primeste mesaje
        buffer = ""
        while True:
            data = conn.recv(4096)
            if not data:
                break

            buffer += data.decode('utf-8')

            # proceseaza mesaje complete (separate prin newline)
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if not line.strip():
                    continue

                message = json.loads(line)

                if message['type'] == 'block':
                    self.received_blocks.append(message['payload'])
                    print(f"[{self.station_name}] primit bloc {message['payload']['block_num'] + 1}/{message['payload']['total_blocks']}")

                    if len(self.received_blocks) == message['payload']['total_blocks']:
                        reassembled = self.splitter.reassemble_message(self.received_blocks)
                        decrypted = self.aes.decrypt(reassembled.decode('utf-8'))
                        print(f"[{self.station_name}] mesaj complet primit: {decrypted}")
                        self.received_blocks = []

                        if callback:
                            callback(decrypted)

        conn.close()
        server.close()

    def connect_and_send(self, target_port, message):
        # conecteaza la alta statie si trimite mesaj
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', target_port))

        print(f"[{self.station_name}] conectat la portul {target_port}")

        # schimb de chei diffie-hellman
        self._key_exchange_client(client)

        # cripteaza mesajul
        encrypted = self.aes.encrypt(message)

        # imparte in blocuri
        blocks = self.splitter.split_message(encrypted)

        print(f"[{self.station_name}] trimit mesajul in {len(blocks)} blocuri")

        # trimite fiecare bloc
        for block in blocks:
            packet = {
                'type': 'block',
                'payload': block
            }
            client.send((json.dumps(packet) + '\n').encode('utf-8'))
            print(f"[{self.station_name}] trimis bloc {block['block_num'] + 1}/{block['total_blocks']}")

        client.close()

    def _key_exchange_server(self, conn):
        # primeste cheia publica
        data = conn.recv(4096)
        other_public_key = int(data.decode('utf-8'))

        # trimite propria cheie publica
        conn.send(str(self.dh.get_public_key()).encode('utf-8'))

        # calculeaza secretul comun
        shared_secret = self.dh.compute_shared_secret(other_public_key)
        self.aes = AESCrypto(shared_secret)

        print(f"[{self.station_name}] schimb de chei finalizat")

    def _key_exchange_client(self, client):
        # trimite cheia publica
        client.send(str(self.dh.get_public_key()).encode('utf-8'))

        # primeste cheia publica
        data = client.recv(4096)
        other_public_key = int(data.decode('utf-8'))

        # calculeaza secretul comun
        shared_secret = self.dh.compute_shared_secret(other_public_key)
        self.aes = AESCrypto(shared_secret)

        print(f"[{self.station_name}] schimb de chei finalizat")
