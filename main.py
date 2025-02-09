import sys

from serve_requests.webserver import run_server as serve_requests_runner
from serve_files.webserver import run_server as serve_files_runner
from atomic_clock.webclient import main as atomic_clock_runner

SERVER_TYPE_TO_ENTRY_POINT = {
    0 : serve_requests_runner,
    1 : serve_files_runner,
    2 : atomic_clock_runner,
}

if __name__ == "__main__":
    # parse out the parameters and option to run which server
    args = sys.argv
    # extract which server needs to be run
    server_type = int(args[1]) if len(args) > 1 else -1

    assert server_type != -1, f'expected server_type to be +ve number, got {server_type}'

    # run the server
    SERVER_TYPE_TO_ENTRY_POINT[server_type]()


