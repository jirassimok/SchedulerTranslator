""" obsolete_partial_parse.py

Author: Jacob Komissar

Date: 2016-04-11

Obsolete versions

Currently, this file does NOT attempt to ignore grad courses.
Uncommenting that bit (the check for length != 4) will not do what I had hoped.
This does not work and causes errors, but I'm not fixing it, because I am
reworking much of the parser from scratch, and this file will be made fully
obsolete by the new parsers.
"""
# TODO: Replace this file (obsolete_partial_parse) and all of its functions.
from json import load as json_load
from json import loads as json_loads
from utility import maybe_print_now


def concatenate_regblocks(pager, output_file, verbose=True):
    """ Writes a full set of regblock jsons to a file.

    The output format is
    {"jsonlist":[regblocks, regblocks, regblocks, ...]}

    @param pager: The pager to get the regblocks with.
    @param output_file: The file to output to.
    @param verbose: If True, progress will be printed.
    """
    regblocks = []
    departments = set()
    for term in pager.termlist:
        # Get departments for the term
        maybe_print_now(verbose, "\nReading term ", term, "...", sep='', end='')
        depts = pager.get(term)
        deptabbrevs = {d["id"] for d in json_loads(depts)}
        departments.union(depts)
        maybe_print_now(verbose, " Success\n")
        # maybe_print_now(verbose, deptabbrevs)
        # Get course listings for each department.
        for dept in deptabbrevs:
            maybe_print_now(verbose, "Reading dept ", dept, "...",
                            sep='', end='')
            courses = [crs["number"] for crs in pager.get_json(term, dept)]
            maybe_print_now(verbose, " Success")
            for cnum in courses:
                # maybe_print_now(True, dept, cnum)
                '''
                if len(cnum)!=4:
                    maybe_print_now(verbose, "\tSkipping", dept, cnum,
                                    ": Course number < 1000")
                    continue
                '''
                maybe_print_now(verbose, "\tFetching", dept + cnum,
                                "regblocks...", end='')
                # maybe_print_now(True, cnum)
                courseregblocks = pager.get(term, dept, cnum, rb=True)
                regblocks.append(courseregblocks)
                maybe_print_now(verbose, " Success")
    # ',\n' would be better for joining regblocks, but I'm done with this file.
    regblocks_str = '"regblocks":[' + ','.join(regblocks) + ']'
    departments_str = '"departments":[' + ','.join(departments) + ']'
    output_json = '{' + regblocks_str + ',' + departments_str + '}'
    with open(output_file, "w+") as file:
        file.write(output_json)


def obs_main_populate_schedb(schedb, input_file, output_file):
    """ Previous main function.
    Obsolete. """
    with open(input_file, "r") as JSON:
        json = json_load(JSON)
    for term in json["departments"]:  # Add departments by term.
        schedb.add_depts(term)
    schedb.obs_convert_list_of_rb_jsons(json["regblocks"])
    with open(output_file, "w+") as SCHEDB:
        SCHEDB.write(str(schedb))
