""" obsolete_partial_parse.py

Author: Jacob Komissar

Date: 2016-04-11

Obsolete versions
"""
# TODO: Replace this file (obsolete_partial_parse) and all of its functions.
# from json import load as json_load
from json import loads as json_loads
from utility import maybe_print_now


def concatenate_regblocks(pager, output_file, verbose=True):
    """ Writes a full set of regblock jsons to a file.

    The output format is
    {"jsonlist":[regblocks, regblocks, regblocks, ...]}

    :param pager: The pager to get the regblocks with.
    :param output_file: The file to output to.
    :param verbose: If True, progress will be printed.
    """
    regblocks = []
    departments = []
    for term in pager.termlist:
        # Get departments for the term
        maybe_print_now(verbose, "\nReading term ", term, "...", sep='', end='')
        depts = pager.get(term)
        deptabbrevs = [d["id"] for d in json_loads(depts)]
        departments.append(depts)
        maybe_print_now(verbose, " Success\n")

        # Get course listings for each department.
        for dept in deptabbrevs:
            maybe_print_now(verbose, "Reading dept ", dept, "...",
                            sep='', end='')
            courses = [crs["number"] for crs in pager.get_json(term, dept)]
            maybe_print_now(verbose, " Success")
            for cnum in courses:
                maybe_print_now(verbose, "\tFetching", dept + cnum, "regblocks...",
                                end='')
                courseregblocks = pager.get(term, dept, cnum, rb=True)
                maybe_print_now(verbose, " Success")
                if '"null"' not in courseregblocks:
                    regblocks.append(courseregblocks)

    regblocks_str = '"regblocks":[' + ','.join(regblocks) + ']'
    departments_str = '"departments":[' + ','.join(departments) + ']'
    output_json = '{' + regblocks_str + ',' + departments_str + '}'
    with open(output_file, "w+") as file:
        file.write(output_json)


def obs_main_populate_schedb(schedb, input_file, output_file):
    """ Previous main function.
    Obsolete. """
    with open(input_file, "r") as JSON:
        string = JSON.read()
    json = json_loads(string)
    for term in json["departments"]:  # Add departments by term.
        schedb.add_depts(term)
    schedb.obs_convert_list_of_rb_jsons(json["regblocks"])
    with open(output_file, "w+") as SCHEDB:
        SCHEDB.write(str(schedb))
