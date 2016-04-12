""" hostdb.py

Author: Jacob Komissar

Date: 2016-04-12

Hosts the local database at port 8000.
"""
# Imports from libraries
import os
from time import sleep
import http.server as server
import threading
# Imports from project
from utility import print_now

SERVER = None


class silentHandler(server.SimpleHTTPRequestHandler):
    """ An http request handler that doesn't send anything to stdout.
    """
    def log_message(self, format, *args):
        return


def run_database_server():
    global SERVER
    base_dir = os.getcwd()

    try:
        os.chdir("../DATABASE")
    except FileNotFoundError as err:
        err.strerror = "Local database not found"
        raise err

    print_now("\nStarting database server...", end='')
    SERVER = server.HTTPServer(('',8000), silentHandler)
    threading.Thread(target=SERVER.serve_forever).start()
    print_now("\tSuccess\n")

    sleep(5)  # Give the server time to start.


def close_database_server():
    global SERVER
    print_now("\nClosing database server...", end='')
    SERVER.shutdown()
    SERVER.socket.close()
    print_now("\tSuccess\n")
