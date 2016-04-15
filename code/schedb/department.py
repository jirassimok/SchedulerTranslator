""" department.py

Author: Jacob Komissar

Date: 2016-04-12

Class to represent departments.

Very much incomplete.
"""
from .course import Course


class Dept(object):
    def __init__(self, abbrev=None, name=None):
        self.abbrev = abbrev
        self.name = name.title()
        self.courses = {}  # indexed by number

    def __str__(self):
        string = ['<dept abbrev="', self.abbrev, '" name="', self.name, '">\n']
        for c in self.courses:
            string.append(str(c))
            string.append("\n")
        string.append("</dept>")
        return ''.join(string)

    def __eq__(self, other):
        """Departments with the same abbreviation are equal."""
        return type(self) is type(other) and self.abbrev == other.abbrev

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_course(self, regblocks, course=None):
        """ Add a course to the department.

        @param regblocks: The regblocks json for the course.
        @param course: The course json
        """
        if not course:
            self.add_course_by_regblocks(self, regblocks)
        else:
            raise NotImplementedError("Dept.add_course can not currently take "
                                      "a course json, as they are unnecessary "
                                      "and would require nearly twice as large "
                                      "a database.")

    def add_course_by_regblocks(self, regblocks):
        pass
