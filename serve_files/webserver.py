
import socket
import sys
import os
from common.common import PACKET_SIZE, listen_server, prepare_body, serve_request

# use the default root, if the path is not found
SERVER_ROOT = os.environ.get('SERVER_ROOT', '~/')

def read_all_data(s):
    """
    Helper method for reading all the data from the packets
    from the open TCP connection, PACKET_SIZE at a time,
    and stitch them together eventually!
    """
    data_ = []

    while data:= s.recv(PACKET_SIZE):
        stop_receiving = False
        data_ = []
        # loop through the data, split by \r\n
        for line in str(data, encoding='utf-8').split('\r\n'):
            if line == "":
                stop_receiving = True
                break

            data_.append(line)

        if stop_receiving:
            break
    
    return data_

def build_http_response_body(file_data):
    """Helper method for building the
    http response body, to be sent to the 
    client
    """

    return prepare_body([
        "HTTP/1.1 200 OK",
        "Content-Type: text/plain",
        f"Content-Length: {len(file_data)}",
        "Connection: close",
        "",
        f"{file_data}"
    ])

def extract_file_name(data):
    """Helper method to extract 
    out the file name from the HTTP
    header
    """
    # find the line, which contains the 'GET' keyword
    http_method_line = None
    for line in data:
        if 'GET' in line:
            http_method_line = line
            break
    
    _, path, _ = http_method_line.split()
    return path

def send_404():
    pass

def read_file_path(file_path):
    """"
    Read the file, and return the strified
    blob
    """
    with open(file_path, 'r') as f:
        return f.read()

def handle_single_request(s):
    """
    Implement the logic to serve the files!
    """

    # accept the request from the new
    # connection
    print('accepting the request....')

    new_socket = s.accept()[0]

    # read the header and the parse out the
    # file which needs to be read

    print('accepted the request....')
    recvd_data = read_all_data(new_socket)

    print(f'received data {recvd_data}')

    # extract out the file_name, that needs to be parsed out
    file_path = extract_file_name(recvd_data)

    # # ensure that we're not serving any files from the root
    # if file_path.startswith(SERVER_ROOT):
    #     send_404()
    print('filepath of the request.....')
    # read the file based on the type of data
    file_data = read_file_path(file_path)

    # build the http response packet and
    # send them back along with the 
    # payload
    data = build_http_response_body(file_data)
    print('http response body.....')


    # send the http response back to
    # the client
    new_socket.sendall(data)
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