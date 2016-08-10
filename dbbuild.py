""" dbbuild.py

Author: Adam Goldsmith
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
import json
from concurrent import futures

# The filename of the local database's directory relative to this directory.


class DbBuilder(object):
    total_courses = 0
    courses_done = 0

    def __init__(self, pager, database, schedb, saving=False,
                 parsing=False, verbose=0, workers=10, delay=0):
        self.pager = pager
        self.database = database
        self.schedb = schedb
        self.saving = saving
        self.parsing = parsing
        self.verbose = verbose
        self.delay = delay
        self.executor = futures.ThreadPoolExecutor(max_workers=workers)

    def vprint(self, *args, **kwargs):
        """ Prints the arguments immediately if self.verbose is true. """
        if self.verbose:
            print(*args, **kwargs, flush=True)

    def print_progress(self):
        if self.total_courses != 0:
            length = 100 # length of the progress bar
            percent = (self.courses_done / self.total_courses)
            progress = int(length * percent)
            pstring = '\r[{}] {}/{} {:.2f}%'.format(("#"*progress).ljust(length),
                                                self.courses_done,
                                                self.total_courses,
                                                percent * 100)
            print(pstring, end='', flush=True)

    def get_page(self, term=None, dept=None, num=None, regblocks=True):
        """ Gets and writes a page to a file.

        @param term: The term to get data for. As last, will fetch dept list.
        @param dept: The department to get. As last, will fetch course list.
        @param num: The course's number. As last, will fetch course information.
        @param regblocks: If true, the course's registration blocks will be fetched.
        """
        # Build the filepath the same way Fetch.get builds a url.
        path = self.pager.create_path(term, dept, num, regblocks)
        # Get the page.
        # print("Fetching:", path)
        page = self.pager.get(path, delay=self.delay)
        if self.saving:  # Write it to the file.
            filepath = self.database + path.replace("%20", " ") + ".json"
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w+") as file:
                file.write(page)

        self.print_progress()

        return json.loads(page)

    def get_course(self, term, deptid, cnum, cinfo=False):
        """ Writes the course listings, details, and regblocks for the given
        department to the files in the test database.

        @param term: The term to fetch data for.
        @param deptid: The department to fetch data for.
        @param cnum: The course to fetch data for.
        @param cinfo: Indicates whether course info besides regblocks is desired.
        """
        self.vprint("\tFetching {}{} Regblocks...".format(deptid, cnum))
        regblocks = self.get_page(term, deptid, cnum)  # Write regblocks
        if self.parsing:
            self.schedb.add_regblocks(regblocks, deptid, cnum)
        if cinfo:  # Write course details
            self.vprint("\t\tCourse info...", end='')
            self.get_page(term, deptid, cnum, regblocks=False)

        self.courses_done += 1

    def get_dept(self, term, deptid, cinfo=False):
        """ Writes the course listings, details, and regblocks for the given
        department to the files in the test database.

        @param term: The term to fetch data for.
        @param deptid: The department to fetch data for.
        @param cinfo: Indicates whether course info besides regblocks is desired.
        """
        self.vprint("Fetching course listings for " + deptid)
        courses = self.get_page(term, deptid)  # Write course listings
        if self.parsing:
            self.schedb.add_courses_to_dept(courses, deptid)

        for course in courses:
            cnum = course["number"]
            self.executor.submit(self.get_course, term, deptid, cnum, cinfo)

    def get_term(self, term, cinfo=False):
        """ Gets all the departments in a term and adds them to the local database.

        @param term: The term to fetch.
        @param cinfo: Indicates whether course info besides regblocks is desired.
        """
        self.vprint("\nFetching term ", term)
        depts = self.get_page(term)
        if self.parsing:
            self.schedb.add_depts(depts)


        self.total_courses += sum([dept["courseCount"] for dept in depts])

        for dept in depts:
            self.get_dept(term, dept["id"], cinfo=cinfo)
        self.vprint("Term", term, "complete\n\n")

    def get_all_terms(self, termlist, prompt=True):
        """ Gets all of the courses in all of the terms in termlist

        @param termlist A list of terms to get
        @param prompt Indicates whether the user should be asked before getting
                      each term..
        """
        self.get_page()  # write terms.json
        for term in termlist:
            if prompt and input("About to fetch term {}, "
                                "enter anything to skip.\n".format(term)):
                continue
            self.get_term(term)
