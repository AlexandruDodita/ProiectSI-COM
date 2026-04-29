#!/usr/bin/env python3

import sys
from secure_station import SecureStation

def main():
    if len(sys.argv) < 2:
        print("utilizare:")
        print("  python demo.py server <port>")
        print("  python demo.py client <target_port> <message>")
        return

    mode = sys.argv[1]

    if mode == "server":
        port = int(sys.argv[2])
        station = SecureStation(port, f"server_{port}")
        print(f"pornesc server pe portul {port}...")
        station.start_server()

    elif mode == "client":
        target_port = int(sys.argv[2])
        message = " ".join(sys.argv[3:])

        station = SecureStation(9999, "client")
        print(f"trimit mesaj catre portul {target_port}: '{message}'")
        station.connect_and_send(target_port, message)
        print("mesaj trimis cu succes")

    else:
        print("mod invalid, foloseste 'server' sau 'client'")

if __name__ == "__main__":
    main()
