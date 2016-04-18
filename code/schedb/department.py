""" department.py

Author: Jacob Komissar

Date: 2016-04-12

Class to represent departments.
"""
from .course import Course


class Dept(object):
    def __init__(self, abbrev=None, name=None):
        self.abbrev = abbrev
        self.name = name.title()
        self.courses = {}  # indexed by number

    def __str__(self):
        string = ['<dept abbrev="', self.abbrev, '" name="', self.name, '">\n']
        for c in self.courses.values():
            string.append(str(c))
            string.append("\n")
        string.append("</dept>")
        return ''.join(string)

    def __eq__(self, other):
        """Departments with the same abbreviation are equal."""
        return type(self) is type(other) and self.abbrev == other.abbrev

    '''
    def add_course(self, coursejson):
        """ Create a course and add it to this department's courses.
        Does not allow duplicate courses.

        @param coursejson: The course json for the course.
        """
        number = coursejson["number"]
        self.courses.setdefault(number, Course(number, coursejson["name"],
                                               dept=self.abbrev))
    '''

    def add_courses(self, courselistjson):
        """ Add a list of courses to this department. Does not allow duplicates.

        @param courselistjson: A course list json.
        """
        for course in courselistjson:
            number = course["number"]
            self.courses.setdefault(number, Course(number, course["title"],
                                                   dept=self.abbrev))

    def add_regblocks(self, regblocks, coursenum):
        """ Add the course/sections/periods represented by the given regblocks
        to the appropriate course in this department.

        @param regblocks: The regblocks json to add.
        @param coursenum: The course's index in this department's course dict.
        """
        self.courses[str(coursenum)].add_regblocks(regblocks)
