""" hostdb.py

Author: Jacob Komissar

Date: 2016-04-12

Status: File complete. Do not edit.

Hosts the local schedule database at ../DATABASE on port 8000.

This file contains four constants, two functions, and a class.

SERVER
    default None
    used to store the server instance
PORT
    default 8000
    specifies the port the server will be hosted from
DATABASE_PATH
    default "../DATABASE"
    the path to the database directory relative to BASE_DIR
BASE_DIR
    the path to the starting directory at import time

def run_database_server()
    Starts the server and stores the instance in SERVER.

def close_database_server()
    Closes the server stored in SERVER.

class silentHandler
    A subclass of http.server.SimpleHTTPRequestHandler that differs only in that
    it does not automatically log requests to stdout.

"""
# Imports from libraries
import os
import sys
from time import sleep
import http.server as server
import threading


SERVER = None  # Will store the server object.
PORT = 8000  # The port to host on.
DATABASE_PATH = "../DATABASE"  # The path to the database.
BASE_DIR = os.getcwd()

class silentHandler(server.SimpleHTTPRequestHandler):
    """ An http request handler that doesn't send anything to stdout.
    """
    def log_message(self, format, *args):
        return


def run_database_server(*, verbose=True):
    """ Runs the server on the port specified by PORT in the directory specified
    by DATABASE_PATH. If the directory does not exist, raises a
    FileNotFoundError.
    The server instance is stored in SERVER.

    @param verbose: Specifies if the function should print values.
    """
    global SERVER

    try:
        os.chdir(DATABASE_PATH)
    except FileNotFoundError as err:
        err.strerror = "Local database not found"
        raise err

    if verbose:
        print("\nStarting database server...", end='')
        sys.stdout.flush()

    SERVER = server.HTTPServer(('',PORT), silentHandler)
    threading.Thread(target=SERVER.serve_forever).start()

    if verbose:
        print("\tSuccess\n")
        sys.stdout.flush()

    sleep(5)  # Give the server time to start.


def close_database_server(*, verbose=True):
    """ Shuts down the server stored in SERVER.
    """
    global SERVER
    if verbose:
        print("\nClosing database server...", end='')
        sys.stdout.flush()
    SERVER.shutdown()
    SERVER.socket.close()
    if verbose:
        print("\tSuccess\n")
        sys.stdout.flush()

    try:
        os.chdir(BASE_DIR)
    except FileNotFoundError as err:
        err.strerror += "\nFatal error: initial directory missing"

