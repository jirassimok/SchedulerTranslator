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
import argparse
# Imports from project.
from schedb.schedb import Schedb
from fetch import Fetch
from dbbuild import DbBuilder  # Only needed to be run once for now.
import hostdb

""" RUN_MODE determines what this program will do. Possible values are:
get - Saves data from a web database to the local database.
parse - Parses data from the local database to a schedb.
"""

parser = argparse.ArgumentParser(description="Retrieves and translates the new "
                                 "Scheduler's database from "
                                 "wpi.collegescheduler.com and writes it to a "
                                 "local database, which can be translated into "
                                 "the old scheduler's schedb xml format.")
parser.add_argument('mode', choices=["get", "parse"],
                    help='The run mode for the program. get creates a local'
                         'database, while parse creates a schedb')
parser.add_argument('--database', default="DATABASE",
                    help='Path for the database (default: %(default)s)')
parser.add_argument('--pwfile', help='A password file')
parser.add_argument('-o', '--output', default="new.schedb",
                    help='Path for the output file (default: %(default)s)')
parser.add_argument('-p', '--port', type=int, default=8000,
                    help='Port for the local database (default: %(default)s)')
parser.add_argument('--prompt', action='store_true',
                    help='Prompt often (default: %(default)s)')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Print extra information (default: %(default)s)')

args = parser.parse_args()

hostdb.PORT = args.port
hostdb.DATABASE_PATH = args.database

# TODO: Make a version of Fetch.get that gets from the file system directly.*
# This would allow unicode to be read much more nicely, I am fairly certain.

if args.mode != "get" and args.mode != "parse":
    raise Exception('Invalid run mode: "' + args.mode + '"')

pager = Fetch(local=(args.mode == "parse"), port=args.port,
              readfile=args.pwfile)
print("Pager initialized")
# pager.set_terms("Fall%202016")
pager.set_terms("Fall%202016", "Summer%202016", "Spring%202017")

if args.mode == "get":
    # Read the external database and write it to the local database.
    dbbuilder = DbBuilder(pager, args.database, args.verbose)
    dbbuilder.term_write_loop(args.prompt)

if args.mode == "parse":
    hostdb.run_database_server()
    pager = Fetch(local=True, port=args.port)
    schedb = Schedb(pager.get_json(pager.create_path())) # initialize with terms

    for term in schedb.terms:
        depts = pager.get_json(pager.create_path(term))
        schedb.add_depts(depts)
        print("Term", term, "deptartments added.")
        for deptjson in depts:
            dept = deptjson["id"]
            courselist = pager.get_json(pager.create_path(term, dept))
            schedb.add_courses_to_dept(courselist, dept)
            print("\tDept", dept, "courses added.")
            for course in courselist:
                number = course["number"]
                regblocks = pager.get_json(pager.create_path(term, dept, number))
                schedb.add_regblocks(regblocks, dept, number)
                print("\t\t", dept, number, "processed.")

    hostdb.close_database_server()

    with open(args.output, mode="w+") as file:
        file.write(str(schedb))
