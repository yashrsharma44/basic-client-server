import socket
import sys
import random

PACKET_SIZE = 4096

def prepare_body(body):
    body = [f"{el}\r\n" for el in body]
    body.append('\r\n')
    return encode_data("".join(body))

def print_status_message(func):

    def wrapper(s):
        func_name = func.__name__
        print(f'starting the function: {func_name}')
        print('------------------------')
        func(s)
        print('------------------------')
        print(f'execution of the function: {func_name} is completed')

    return wrapper

def encode_data(data):
    return bytes(data, encoding='utf-8')

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

@print_status_message
def serve_request(s):
    """
    Helper method to handle the requests
    from different clients
    """
    while True:
        handle_single_request(s)

@print_status_message
def listen_server(s):
    """
    Helper function to setup web-server!
    """
    s.listen()

if __name__ == "__main__":
    args = sys.argv
    port = args[1] if len(args) > 1 else 20123

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))

    listen_server(s)
    serve_request(s)

    
    