
PACKET_SIZE = 4096

def prepare_body(body):
    body = [f"{el}\r\n" for el in body]
    body.append('\r\n')
    return encode_data("".join(body))


def print_status_message(func):

    def wrapper(s, *args, **kwargs):
        func_name = func.__name__
        print(f'starting the function: {func_name}')
        print('------------------------')
        func(s, *args, **kwargs)
        print('------------------------')
        print(f'execution of the function: {func_name} is completed')

    return wrapper

def encode_data(data):
    return bytes(data, encoding='utf-8')

@print_status_message
def serve_request(s, handler):
    """
    Helper method to handle the requests
    from different clients
    """
    while True:
        handler(s)

@print_status_message
def listen_server(s):
    """
    Helper function to setup web-server!
    """
    s.listen()
