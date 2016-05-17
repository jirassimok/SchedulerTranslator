#!/usr/bin/env python3
""" Main.py

Author: Jacob Komissar

Date: 2016-04-12

Running this file will read all departments and courses in the local
database to a schedb, and print all the departments and regblocks into
io/regblockslist.json, then read that and write a schedb to
io/new_v1.1.schedb.

"""
# Imports from libraries.
import sys
# Imports from project.
from schedb.schedb import Schedb
from fetch import Fetch
from tdbbuild import term_write_loop  # Only needed to be run once for now.
import partial_parse
import hostdb
# import utility

""" RUN_MODE determines what this program will do. Possible values are:
get - Saves data from a web database to the local database.
parse - Parses data from the local database to a schedb.
"""

IO_PATH = "io"
# There are many better ways to do this, but this is not my top priority.
if len(sys.argv)>1:  # If command line arguments found...
    RUN_MODE = sys.argv[1]
    if RUN_MODE == "parse":
        sys.exit()
    if len(sys.argv)>2:
        hostdb.PORT = sys.argv[2]
        PORT = sys.argv[2]
        if len(sys.argv)>3:
            hostdb.DATABASE_PATH = sys.argv[3]
            if len(sys.argv)>4:
                IO_PATH = sys.argv[4]

else:
    raise Exception('No run mode specified.')

IO_PATH = IO_PATH.rstrip("/")
JSON_FILE = IO_PATH + "/regblockslist.json"
SCHEDB_FILE = IO_PATH + "/new_v1.1.schedb"

# TODO: Make a version of Fetch.get that gets from the file system directly.*
# This would allow unicode to be read much more nicely, I am fairly certain.

if RUN_MODE != "get" and RUN_MODE != "parse":
    raise Exception('Invalid run mode: "' + RUN_MODE + '"')

pager = Fetch(local=(RUN_MODE == "parse"), port=PORT)  # readfile=None
print("Pager initialized")
# pager.set_terms("Fall%202016")
pager.set_terms("Fall%202016", "Summer%202016", "Spring%202017")

if RUN_MODE == "get":
    # Read the external database and write it to the local database.
    term_write_loop(pager, prompt=False)

if RUN_MODE == "parse":
    schedb = Schedb()
    hostdb.run_database_server()
    partial_parse.concatenate_regblocks(pager, JSON_FILE, verbose=False)
    partial_parse.obs_main_populate_schedb(
        schedb, JSON_FILE, SCHEDB_FILE)
    hostdb.close_database_server()  # Stop the database server.
