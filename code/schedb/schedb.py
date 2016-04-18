""" schedjson.py

Author: Jacob Komissar

Date: 2016-04-10

Self-parsing schedb classes file.

Temporarily put on hold to complete the lesser version of the functions in time
for course registration.

"""
from .department import Dept
from time import strftime


class Schedb(object):
    def __init__(self, termsjson=None):
        self.terms = []  # List because nothing to index by. - could be a set
        self.depts = {}
        self.xmlns = "https://scheduler.wpi.edu"
        self.schemaLocation = "https://scheduler.wpi.edu schedb.xsd"

        if termsjson:
            self.add_terms(termsjson)

    def __str__(self):
        string = ['<?xml version="1.0" encoding="UTF-8"?>\n'
                  '<schedb xmlns="', self.xmlns, '" '
                  'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                  'xsi:schemaLocation="', self.schemaLocation, '" '
                  'generated="', strftime("%a %b %d %H:%M:%S %Y").upper(), '" '
                  'minutes-per-block="30">\n']
        depts = self.sort_depts()

        for dept in depts:
            string.append(str(dept))
            string.append("\n")
        string.append("</schedb>")
        return ''.join(string)

    def sort_depts(self):
        orderlist = Dept.get_order()  # The grand sorting list for departments.
        depts = []
        for key in self.depts.keys():
            if key in orderlist:
                depts.append(self.depts[key])  # filter out invalid departments
        return sorted(depts)  # works because Dept.__lt__ is implemented.

    def add_terms(self, termsjson):
        """ Add a list of terms to this schedb. Prevents duplicates.
        Currently ignores summer.
        @param termsjson: A term list json.
        """
        for term in termsjson:
            termstring = term["id"]  # could also use term["title"]
            if termstring not in self.terms and "Summer" not in termstring:
                self.terms.append(termstring)

    def add_depts(self, deptlistjson):
        """ Add a list of departments to this schedb. Prevents duplicates.

        @param deptlistjson: A department list json.
        """
        for dept in deptlistjson:
            abbrev = dept["id"]  # Could use short, but id is more likely unique
            self.depts.setdefault(abbrev, Dept(abbrev, dept["long"]))

    def add_courses_to_dept(self, courselistjson, dept):
        """ Add the course listings in the given json to the appropriate dept in
        this Schedb's depts.

        @param courselistjson: A course list json.
        @param dept: The abbreviation for the department the course is in.
        """
        self.depts[dept].add_courses(courselistjson)

    def add_regblocks(self, regblocks, dept, coursenum):
        """ Add the course/sections/periods represented by the given regblocks
        to the appropriate department/course in this Schedb.

        @param regblocks: The regblocks json to add.
        @param dept: The abbreviation for the department the course is in.
        @param coursenum: The course's number in its department.
        """
        self.depts[dept].add_regblocks(regblocks, str(coursenum))

    ''' I don't need to worry about mixed departments (yet, at least).
    def add_courses(self, courselistjson, *, dept=None):
        """ Add the courses listings in the given json to this Schedb's depts.

        @param courselistjson: A course list json.
        @param singledept: If True, all courses are assumed to be in the same
                           department.
        """
        if singledept:
            self.add_courses_to_dept(courselistjson)
        else:
            for course in courselistjson:
                dept = self.depts[courselistjson["subectId"]]
                dept.add_course(course)
    '''
