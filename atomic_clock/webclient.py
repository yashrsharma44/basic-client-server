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

    host = args[2] if len(args) > 2 else 'example.com'
    port = int(args[3]) if len(args) > 3 else 80

    print(f"connecting to {host}:{port}")
    socket_ = socket.socket()
    socket_.connect((
        host,
        port
    ))

    # send the bytes to the server
    socket_.sendall(bytes())

    while data := socket_.recv(PACKET_SIZE):
        # received data is the current time since 1st Jan
        # 1970; the data received is in the big-endian format
        print(int.from_bytes(data, 'big'))


if __name__ == "__main__":
    main()