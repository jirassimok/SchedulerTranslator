""" tdbbuild.py

Author: Jacob Komissar

Date: 2016-04-10

Function for easier construction of test database.

Structure of the test database:
DATABASE/
         terms.json
         terms/
               Season YEAR/
                           subjects.json
                           subjects/
                                    DEPT/
                                         courses.json
                                         courses/
                                                 NUMBER/
                                                        regblocks.json
                                                 NUMBER...
                                    DEPT...
               Season YEAR...
"""
import os
import sys
from utility import maybe_print_now

# The filename of the local database's directory relative to this directory.
LOCAL_DATABASE = "DATABASE"
DEFAULT_DIR = os.getcwd()

def get_coursenums(fetch, term, dept):
    """ Returns a list of the course numbers for the given department.
    @param fetch: The Fetch object to use to get the course numbers.
    @param term: The term to get course numbers during.
    @param dept: The department to list courses for.
    """
    courses = fetch.get_json(fetch.create_path(term, dept))
    return [course["number"] for course in courses]


def write_page(fetch, term=None, dept=None, num=None,
               *, regblocks=True, delay=0.0):
    """ Gets and writes a page to a file.

    @param fetch: A Fetch object to use to get the pages.
    @param term: The term to get data for. As last, will fetch dept list.
    @param dept: The department to get. As last, will fetch course list.
    @param num: The course's number. As last, will fetch course information.
    @param regblock: If true, the course's registration blocks will be fetched.
    @param delay: How long to wait before getting the page.
    """
    # Build the filepath the same way Fetch.get builds a url.
    path = fetch.create_path(term, dept, num, regblocks)
    # Get the page.
    # print("Fetching:", path)
    page = fetch.get(path, delay=delay)
    # Write it to the file.
    filepath = LOCAL_DATABASE + path.replace("%20", " ") + ".json"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w+") as file:
        file.write(page)

def write_dept(fetch, term, dept, *, cinfo=False,
               delay=0.0, verbose=True):
    """ Writes the course listings, details, and regblocks for the given
    department to the files in the test database.
    @param fetch: The Fetch object to get the data with.
    @param term: The term to fetch data for.
    @param dept: The department to fetch data for.
    @param cinfo: Indicates whether course info besides regblocks is desired.
    @param delay: How long to wait between requests.
    """
    maybe_print_now(verbose, "Fetching course listings for " + dept + "...",
                    sep='', end='')
    # Write course listings
    write_page(fetch, term, dept, delay=0)
    maybe_print_now(verbose, "\tSuccess")
    coursenums = get_coursenums(fetch, term, dept)
    for cnum in coursenums:
        maybe_print_now(verbose, "\tFetching " + dept + cnum + " Regblocks...",
                        sep='', end='')
        # Write regblocks
        write_page(fetch, term, dept, cnum, delay=delay)
        maybe_print_now(verbose, "\tSuccess")
        if cinfo:
            maybe_print_now(verbose, "\t\tCourse info...", end='')
            # Write course details
            write_page(fetch, term, dept, cnum, regblocks=False)
            maybe_print_now(verbose, "\tSuccess")


def write_term(pager, term, *, cinfo=False,
               verbose=True):
    """ Gets all the departments in a term and adds them to the local database.
    @param pager: The Fetch object to get the data with.
    @param term: The term to fetch.
    @param cinfo: Indicates whether course info besides regblocks is desired.
    """
    maybe_print_now(verbose, "\nFetching term ", term, "...\n", sep="")
    write_page(pager, term)
    depts = pager.get_json(pager.create_path(term))  # Get dept listings for term.
    depts = [d["id"] for d in depts]  # save the abbrevs we'll need to loop on
    for dept in depts:
        write_dept(pager, term, dept, cinfo=cinfo,
                   delay=0.0, verbose=verbose)
    maybe_print_now(verbose, "Term", term, "complete\n\n")

def term_write_loop(pager, *, prompt=True, verbose=True):
    write_page(pager) # write terms.json
    for term in pager.termlist:
        if prompt and input("About to fetch term {}.\n".format(term) +
                            "Enter anything to skip.\n"):
            continue
        write_term(pager, term, cinfo=False, verbose=verbose)
