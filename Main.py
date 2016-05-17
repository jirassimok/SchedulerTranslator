#!/usr/bin/env python3
""" Main.py

Author: Jacob Komissar

Date: 2016-04-12

Running this file will read all departments and courses in the local database
(which must be running on port 8000) to a schedb, and print all the departments
and regblocks in to io/regblockslist.json, then read that and write a schedb
to io/new_v1.1.schedb.

ONLY RUN THIS FILE IN "get" MODE.

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

# DONE: Create a set of classes to represent the json structure.
# Using algorithms similar to the web->file database reader,
# Make a web->object database reader.
# DONE: Then pass a schedbparse to the schedb to parse.
# DONE: Fix labs/conferences AFTER classes get me easy access to all the data.

# TODO: Make a version of Fetch.get that gets from the file system directly.*
# This would allow unicode to be read much more nicely, I am fairly certain.

'''
Plans:

The next major version of Translator.py will be called jsonParser.py.

If I ever redo this, I hope to further separate the Fetcher from the Parser.

Anything preceded by "#" in these plans is to be skipped

#1. jF will get term info.
#2. MANUALLY select a term. (if automatic, in this file or its own file)
#    2.1 Term info ("code") will be passed along the parsechain.

1. MANUALLY get term root URL with department list.
2. jsonFetcher will get the department list
3. Parse that to python with json.loads
4. Add depts to the schedb.
4. Grab ["id"]s
5. Create Dept objects
6. Loop over depts:

For each department:
7. jsonFetcher gets course list and passes it to the schedb
8. The schedb loops over the courselist
9. For each course, the schedb passes it to the correct Dept
10. The dept adds the courses as incomplete course objects
11. Grab course number lists. [x["id"].split("|")[1] for x in courselist]
12. Loop over those to get regblocks


In here, I could get the course info pages, but the regblocks have enough.

12. jsonFetcher gets regblocks
Regblock parsing:
1. start with a regblocks json
2. get ["sections"]
3. sort from list to dictionary, using ["id"] (CRN) as key
2. get ["registrationBlocks"]
3. Loop over them:
4.   add a section
5.   add a section and period to the course for each thing in ["sectionIds"]
6.


4. The Term's department dictionary's keys will be looped over. Each time:
5. jsonFetcher will place the course list for the department in a file.


Mismatches between formats:

course: schedb has min-/max-credits and grade-type
section: lots

'''
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
