import socket
import sys
import random

from common.common import PACKET_SIZE, encode_data, listen_server, print_status_message, serve_request


def prepare_body(body):
    body = [f"{el}\r\n" for el in body]
    body.append('\r\n')
    return encode_data("".join(body))


@print_status_message
def handle_single_request(s):
    """Helper method for handling
    a single request!
    """
    new_socket = s.accept()[0]

    while data := new_socket.recv(PACKET_SIZE):
        
        stop_receiving = False
        data_ = []
        # loop through the data, split by \r\n
        for line in str(data, encoding='utf-8').split('\r\n'):
            if line == "":
                stop_receiving = True
                break

            data_.append(line)

        # print the data received
        print("\n".join(data_))
        print('------------------------')

        if stop_receiving:
            break
    
    # send a response from the server
    new_socket.sendall(prepare_body([
        "HTTP/1.1 200 OK",
        "Content-Type: text/plain",
        "Content-Length: 20",
        "Connection: close",
        "",
        f"Hello! {random.random()}"
    ]))
    new_socket.close()


if __name__ == "__main__":
    args = sys.argv
    port = args[1] if len(args) > 1 else 20123

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))

    listen_server(s)
    serve_request(s, handle_single_request)

    
    