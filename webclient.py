import json
import socket

import sys



PACKET_SIZE = 4096

def create_body(hostname):

    request_body = ("GET / HTTP/1.1\r\n"
    f"Host: {hostname}\r\n"
    "Connection: close\r\n"
    "\r\n")

    return bytes(request_body, encoding='utf-8')

def main():
    args = sys.argv

    host = args[1] if len(args) > 1 else 'example.com'
    port = args[2] if len(args) > 2 else 80

    request_body = create_body(host)

    print(f"connecting to {host}:{port}")
    socket_ = socket.socket()
    socket_.connect((
        host,
        port
    ))

    # send the bytes to the server
    socket_.sendall(request_body)

    while data := socket_.recv(PACKET_SIZE):
        print(data)


if __name__ == "__main__":
    main()