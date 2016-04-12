""" dept.py

Author: Jacob Komissar

Date: 2016-04-10

File for the Dept class.
"""
from .coursec import Course


class Dept(object):
    def __init__(self, abbrev=None, name=None):
        self.abbrev = abbrev
        self.name = name.title()
        self.courses = []

    def __str__(self):
        strng = '<dept abbrev="' + self.abbrev + '" name="' + self.name + '">\n'
        for c in self.courses:
            strng += str(c) + "\n"
        return strng + '</dept>'

    def __eq__(self, other):
        """Departments with the same abbreviation are equal."""
        return isinstance(other, Dept) and self.abbrev == other.abbrev

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_courses(self, json):
        pass

    def add_course(self, course_info_json):
        pass

    def parse_course(self, json):
        """ Obsolete.
        :param json: the course json to parse"""
        course = Course()
        course.parse_self(json)
        course.parse_sections(json)
        self.courses.append(course)

    def semiobs_add_course(self, course):
        # if course not in self.courses:  # seems to check with ==
        #     self.courses.append(course)
        # else:
        for c in self.courses:
            if c==course and c.islabs==course.islabs:
                c.sections.extend(course.sections)
                break  # No need to go on after adding the course.
        else:  # If the course/labs was not found.
            self.courses.append(course)
