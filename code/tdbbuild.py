""" tdbbuild.py

Author: Jacob Komissar

Date: 2016-04-10

Function for easier construction of test database.s
"""
import os
from utility import maybe_print_now

# The filename of the local database's directory relative to this directory.
LOCAL_DATABASE = "../DATABASE/"
DEFAULT_DIR = os.getcwd()


def reset_dir():
    """ Resets working directory. """
    os.chdir(DEFAULT_DIR)


def set_dir():
    """ Set working directory so write_page works properly.
    DO NOT call this more than once.
    """
    try:
        os.chdir(LOCAL_DATABASE)
    except FileNotFoundError as err:
        print("\n\nBe careful using tdbbuild in your file system. It was not"
              "designed with your file system in mind, and it does quite a bit"
              "of directory and file creation.\n\n")
        raise err


def get_coursenums(fetch, term, dept):
    """ Returns a list of the course numbers for the given department.
    @param fetch: The Fetch object to use to get the course numbers.
    @param term: The term to get course numbers during.
    @param dept: The department to list courses for.
    """
    courses = fetch.get_json(term, dept)
    return [course["number"] for course in courses]


def write_page(fetch, term, dept=None, num=None, regblock=None,
               *, in_dir=False, delay=0.0):
    """ Gets and writes a page to a file.

    The term directory must exist beforehand, but all others need not exist.

    @param fetch: A Fetch object to use to get the pages.
    @param term: The term to get data for. As last, will fetch dept list.
    @param dept: The department to get. As last, will fetch course list.
    @param num: The course's number. As last, will fetch course information.
    @param regblock: If true, the course's registration blocks will be fetched.
    @param in_dir: If true, the directory will not be changed.
    @param delay: How long to wait before getting the page.
    """
    if not in_dir:
        set_dir()
    # Build the filepath the same way Fetch.get builds a url.
    filepath = LOCAL_DATABASE + term.replace("%20", " ") + "/subjects"
    if dept:
        filepath += "/" + dept + "/courses"
        if not os.path.exists(filepath):
            os.makedirs(filepath)  # Ensure presence of courses directory.
        if num:
            filepath += "/" + str(num)
            if not os.path.exists(filepath):
                os.makedirs(filepath)  # Ensure presence of course directory.
            if regblock:
                filepath += "/regblocks"
    filepath += ".json"
    # Get the page.
    page = fetch.get(term, dept, num, regblock, delay=delay)
    # Write it to the file.
    with open(filepath, "w+") as file:
        file.write(page)
    if not in_dir:
        reset_dir()


def write_dept(fetch, term, dept,
               *, cinfo=False, in_dir=False, delay=0.0, verbose=True):
    """ Writes the course listings, details, and regblocks for the given
    department to the files in the test database.
    @param fetch: The Fetch object to get the data with.
    @param term: The term to fetch data for.
    @param dept: The department to fetch data for.
    @param cinfo: Indicates whether course info besides regblocks is desired.
    @param in_dir: If true, the directory will not be changed.
    @param delay: How long to wait between requests.
    """
    maybe_print_now(verbose, "Fetching course listings for " + dept + "...",
                    sep='', end='')
    # Write course listings
    write_page(fetch, term, dept, in_dir=in_dir, delay=0)
    maybe_print_now(verbose, "\tSuccess")
    coursenums = get_coursenums(fetch, term, dept)
    for cnum in coursenums:
        maybe_print_now(verbose, "\tFetching " + dept + cnum + " Regblocks...",
                  sep='', end='')
        # Write regblocks
        write_page(fetch, term, dept, cnum, True,
                   in_dir=in_dir, delay=delay)
        maybe_print_now(verbose, "\tSuccess")
        if cinfo:
            maybe_print_now(verbose, "\t\tCourse info...", end='')
            # Write course details
            write_page(fetch, term, dept, cnum, False, in_dir=in_dir)
            maybe_print_now(verbose, "\tSuccess")


def write_term(pager, term, *, cinfo=False, in_dir=False, verbose=True):
    """ Gets all the departments in a term and adds them to the local database.
    @param pager: The Fetch object to get the data with.
    @param term: The term to fetch.
    @param cinfo: Indicates whether course info besides regblocks is desired.
    @param in_dir: If true, the directory will not be changed.
    """
    maybe_print_now(verbose, "\nFetching term ", term, "...\n", sep="")
    write_page(pager, term, in_dir=in_dir)
    depts = pager.get_json(term)  # Get dept listings for term.
    depts = [d["id"] for d in depts]  # save the abbrevs we'll need to loop on
    for dept in depts:
        write_dept(pager, term, dept,
                   cinfo=cinfo, in_dir=in_dir, delay=0.0, verbose=verbose)
    maybe_print_now(verbose, "Term", term, "complete\n\n")


def write_term_to_database(pager, term, *, verbose=True):
    """ Moves to the database directory, writes the term data, and moves back.
    @param pager: The Fetch object to get the data with.
    @param term: The term to fetch.
    """
    set_dir()
    write_term(pager, term, cinfo=False, in_dir=True, verbose=verbose)
    reset_dir()


def term_write_loop(pager, *, prompt=True, verbose=True):
    if prompt:
        for term in pager.termlist:
            if not input("About to fetch term " + term + ".\n"
                         "Enter anything to skip.\n"):
                write_term_to_database(pager, term, verbose=verbose)
    else:  # if not prompt
        for term in pager.termlist:
                write_term_to_database(pager, term, verbose=verbose)
