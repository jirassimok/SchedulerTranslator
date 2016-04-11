""" Main.py

Author: Jacob Komissar

Date: 2016-04-09/10

Running this file will read all departments and courses in the local database
(which must be running on port 8000) to a schedb, and print all the departments
and regblocks in to ../io/regblockslist.json, then read that and write a schedb
to ../io/new_v1.1.schedb.
"""
from schedb.schedb import Schedb
from json_fetcher import Fetch
# from tdbbuild import term_write_loop  # Only needed to be run once for now.
import obsolete_partial_parse

BUILDING_JSON = False
BUILDING_SCHEDB = True

INPUT_FILE = "../io/regblockslist.json"
OUTPUT_FILE = "../io/new_v1.1.schedb"

PICKLE = True
PICKLE_FILE = "FILE_SHOULD_NOT_EXIST_PLEASE_DELETE"
if PICKLE:
    import pickle
    PICKLE_FILE = "../io/schedb.pickle"

# TODO: Create a set of classes to represent the json structure.
# Using algorithms similar to the web->file database reader,
# Make a web->object database reader.
# TODO: Then pass a schedjson to the schedb to parse.
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

schedb = Schedb()
pager = Fetch(local=False)  # readfile=None
print("Pager initialized")
# pager.set_terms("Fall%202016")
pager.set_terms("Fall%202016", "Summer%202016", "Spring%202017")


def get_and_list_depts(schedb, pager):
    depts = pager.get_json(pager.term)
    schedb.add_depts(depts)
    for d, D in schedb.departments.items():
        print(d, "\t", D.abbrev, "\t", D.name, sep='')


if BUILDING_JSON:
    obsolete_partial_parse.concatenate_regblocks(pager, INPUT_FILE)
if BUILDING_SCHEDB:
    obsolete_partial_parse.obs_main_populate_schedb(
        schedb, INPUT_FILE, OUTPUT_FILE)

if PICKLE:
    # Save the object for no particular reason. The file must already exist.
    with open(PICKLE_FILE, "wb") as pfile:
        pickle.dump(schedb, pfile)




'''# This is the code I'm currently working on.

depts = pager.get_json(pager.term)
schedb.add_depts(depts)
depts = [d["id"] for d in depts]  # save the abbreviations we'll need to loop on

for dept in depts:
    courses = pager.get_json(pager.term, dept)
    coursnums = [course["number"] for course in courses]
    # Do a hell of a lot more in this loop - quite possible everything?
#'''



