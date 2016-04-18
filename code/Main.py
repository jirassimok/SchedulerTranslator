#!/usr/bin/env python3
""" Main.py

Author: Jacob Komissar

Date: 2016-04-12

Running this file will read all departments and courses in the local database
(which must be running on port 8000) to a schedb, and print all the departments
and regblocks in to ../io/regblockslist.json, then read that and write a schedb
to ../io/new_v1.1.schedb.

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

IO_PATH = "../io"
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
    RUN_MODE = "unspecified"
    PORT = 8000

IO_PATH = IO_PATH.rstrip("/")
JSON_FILE = IO_PATH + "/regblockslist.json"
SCHEDB_FILE = IO_PATH + "/new_v1.1.schedb"

# TODO: Create a set of classes to represent the json structure.
# Using algorithms similar to the web->file database reader,
# Make a web->object database reader.
# TODO: Then pass a schedbparse to the schedb to parse.
# TODO: Fix labs/conferences AFTER classes get me easy access to all the data.

# TODO: MAJOR ISSUES: Can't parse anything including "null". (explicitly)

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
if RUN_MODE == "get":
    # Setup for pager
    READING_DATABASE = True  # Should always be true as of 2016-04-12
    DATABASE_IS_LOCAL = False

    # Setup for database retrieval
    WRITING_LOCAL_DATABASE = True

    # Setup for file-reading/writing
    BUILDING_JSON = False
    BUILDING_SCHEDB = False
elif RUN_MODE == "parse":
    READING_DATABASE = True  # Should always be true as of 2016-04-12
    DATABASE_IS_LOCAL = True

    WRITING_LOCAL_DATABASE = False

    BUILDING_JSON = True
    BUILDING_SCHEDB = True
elif RUN_MODE == "unspecified":
    raise Exception('No run mode specified.')
else:
    raise Exception('Invalid run mode: "' + RUN_MODE + '"')


def get_and_list_depts(_schedb, _pager):
    depts = _pager.get_json(pager.term)
    _schedb.add_depts(depts)
    for d, D in _schedb.departments.items():
        print(d, "\t", D.abbrev, "\t", D.name, sep='')


schedb = Schedb()
if READING_DATABASE:
    pager = Fetch(local=DATABASE_IS_LOCAL, port=PORT)  # readfile=None
    print("Pager initialized")
    # pager.set_terms("Fall%202016")
    pager.set_terms("Fall%202016", "Summer%202016", "Spring%202017")
    if DATABASE_IS_LOCAL:
        hostdb.run_database_server()

if READING_DATABASE and BUILDING_JSON:
    partial_parse.concatenate_regblocks(pager, JSON_FILE, verbose=False)
if BUILDING_SCHEDB:
    partial_parse.obs_main_populate_schedb(
        schedb, JSON_FILE, SCHEDB_FILE)

if READING_DATABASE and WRITING_LOCAL_DATABASE:  # Read the external database,
    term_write_loop(pager, prompt=False)  # and write it to the local database.

if READING_DATABASE and DATABASE_IS_LOCAL:
    hostdb.close_database_server()  # Stop the database server.

'''# This is the code I'm currently working on.

depts = pager.get_json(pager.term)
schedb.add_depts(depts)
depts = [d["id"] for d in depts]  # save the abbreviations we'll need to loop on

for dept in depts:
    courses = pager.get_json(pager.term, dept)
    coursnums = [course["number"] for course in courses]
    # Do a hell of a lot more in this loop - quite possible everything?
#'''
