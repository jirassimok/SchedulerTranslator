""" dbbuild.py

Author: Jacob Komissar

Date: 2016-04-10

Class for building a local database

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
from utility import maybe_print_now

# The filename of the local database's directory relative to this directory.

class DbBuilder(object):

    def __init__(self, pager, database, verbose=False):
        self.pager = pager
        self.database = database
        self.verbose = verbose

    def get_coursenums(self, term, dept):
        """ Returns a list of the course numbers for the given department.
        @param term: The term to get course numbers during.
        @param dept: The department to list courses for.
        """
        courses = self.pager.get_json(self.pager.create_path(term, dept))
        return [course["number"] for course in courses]


    def write_page(self, term=None, dept=None, num=None,
                   *, regblocks=True, delay=0.0):
        """ Gets and writes a page to a file.

        @param term: The term to get data for. As last, will fetch dept list.
        @param dept: The department to get. As last, will fetch course list.
        @param num: The course's number. As last, will fetch course information.
        @param regblock: If true, the course's registration blocks will be fetched.
        @param delay: How long to wait before getting the page.
        """
        # Build the filepath the same way Fetch.get builds a url.
        path = self.pager.create_path(term, dept, num, regblocks)
        # Get the page.
        # print("Fetching:", path)
        page = self.pager.get(path, delay=delay)
        # Write it to the file.
        filepath = self.database + path.replace("%20", " ") + ".json"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w+") as file:
            file.write(page)

    def write_dept(self, term, dept, *, cinfo=False,
                   delay=0.0):
        """ Writes the course listings, details, and regblocks for the given
        department to the files in the test database.
        @param term: The term to fetch data for.
        @param dept: The department to fetch data for.
        @param cinfo: Indicates whether course info besides regblocks is desired.
        @param delay: How long to wait between requests.
        """
        maybe_print_now(self.verbose, "Fetching course listings for " + dept + "...",
                        sep='', end='')
        # Write course listings
        self.write_page(term, dept, delay=0)
        maybe_print_now(self.verbose, "\tSuccess")
        coursenums = self.get_coursenums(term, dept)
        for cnum in coursenums:
            maybe_print_now(self.verbose, "\tFetching " + dept + cnum + " Regblocks...",
                            sep='', end='')
            # Write regblocks
            self.write_page(term, dept, cnum, delay=delay)
            maybe_print_now(self.verbose, "\tSuccess")
            if cinfo:
                maybe_print_now(self.verbose, "\t\tCourse info...", end='')
                # Write course details
                self.write_page(term, dept, cnum, regblocks=False)
                maybe_print_now(self.verbose, "\tSuccess")


    def write_term(self, term, *, cinfo=False):
        """ Gets all the departments in a term and adds them to the local database.
        @param term: The term to fetch.
        @param cinfo: Indicates whether course info besides regblocks is desired.
        """
        maybe_print_now(self.verbose, "\nFetching term ", term, "...\n", sep="")
        self.write_page(self.pager, term)
        depts = self.pager.get_json(self.pager.create_path(term))  # Get dept listings for term.
        depts = [d["id"] for d in depts]  # save the abbrevs we'll need to loop on
        for dept in depts:
            self.write_dept(term, dept, cinfo=cinfo, delay=0.0)
        maybe_print_now(self.verbose, "Term", term, "complete\n\n")

    def term_write_loop(self, prompt=True):
        self.write_page() # write terms.json
        for term in self.pager.termlist:
            if prompt and input("About to fetch term {}.\n".format(term) +
                                "Enter anything to skip.\n"):
                continue
            self.write_term(term, cinfo=False)
