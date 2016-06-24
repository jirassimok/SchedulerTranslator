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

parser = argparse.ArgumentParser(description="Retrieves and translates the new "
                                 "Scheduler's database from "
                                 "wpi.collegescheduler.com and writes it to a "
                                 "local database, which can be translated into "
                                 "the old scheduler's schedb xml format.")
parser.add_argument('--database', default="DATABASE",
                    help='Path for the database (default: %(default)s)')
parser.add_argument('--pwfile', help='A password file (username on the first line, password on the next)')
parser.add_argument('-o', '--output', default="new.schedb",
                    help='Path for the output file (default: %(default)s)')
parser.add_argument('--prompt', action='store_true',
                    help='Prompt often (default: %(default)s)')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Print extra information (default: %(default)s)')
parser.add_argument('-l', '--local', action='store_true',
                    help='Use the local database generated with "-g" (default: %(default)s)')
parser.add_argument('-g', '--get', action='store_true',
                    help='Generate a local database for use with "-l" (default: %(default)s)')
parser.add_argument('--no-parse', action='store_true',
                    help='Don\'t parse the data. Implies "-g" (default: %(default)s)')


args = parser.parse_args()

pager = Fetch(local=(args.database if args.local else None),
              readfile=args.pwfile)
print("Pager initialized")
pager.set_terms("Fall%202016", "Spring%202017")

schedb = Schedb(pager.get_json(pager.create_path())) # initialize with terms
dbbuilder = DbBuilder(pager, args.database, schedb,
                      saving=args.get or args.no_parse,
                      parsing=(not args.no_parse),
                      verbose=args.verbose)
dbbuilder.get_all_terms(args.prompt)

if not args.no_parse:
    with open(args.output, mode="w+") as file:
        file.write(str(schedb))
