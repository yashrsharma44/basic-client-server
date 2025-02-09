import socket
import sys
import random

from common.common import PACKET_SIZE, listen_server, prepare_body, print_status_message, serve_request

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

def run_server():

    port = 20123

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))

    listen_server(s)
    serve_request(s, handle_single_request)

if __name__ == "__main__":
    run_server()