""" schedb.py

Author: Jacob Komissar

Date: 2016-04-10

Schedb class file.

Defines the Schedb class, which can be used to represent xml files in the
schedb format.

The Schedb class was originally called School, and briefly Term.
"""
from time import strftime
from .dept import Dept
from . import parser


class Schedb(object):
    def __init__(self):
        self.departments = {}  # This doesn't need to be in __init__...

    def __str__(self):
        string = ('<?xml version="1.0" encoding="UTF-8"?>\n<schedb '
                  'xmlns="https://scheduler.wpi.edu" '
                  'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                  'xsi:schemaLocation="https://scheduler.wpi.edu schedb.xsd" '
                  'generated="')
        string += strftime("%a %b %d %H:%M:%S %Y").upper()
        string += '" minutes-per-block="30">\n'
        for N, dept in self.departments.items():
            string += str(dept) + "\n"
        string += "</schedb>"
        return string

    def add_dept(self, abbrev, name):
        """ Adds the specified department if it is not already there.

        :param abbrev: The department's abbreviation.
        :param name: The department's ƒull name."""
        self.departments.setdefault(abbrev, Dept(abbrev, name))

    def add_depts(self, json):
        """ Parses a department list json into self.departments.
        :param json: A list of dictionaries representing the department list.
        """
        for d in json:
            self.add_dept(d["id"], d["long"])

    def add_dept_courses(self, json):
        """ Passes a course listing json to the appropriate department.

        :param json: A departments course listing json.
        """
        dept = json["subjectId"]
        if dept in self.departments:
            self.departments[dept].add_courses(json)
        else:
            raise KeyError('No department "' + dept + '" found.')

    # TODO: Add a validation method to remove incomplete children from Schedbs.

    def add_courses_to_dept(self, dept, courses):
        """ Adds courses to dept.

        :param dept: The department id to add courses to.
        :param courses: The course list to add.
        """
        self.departments[dept].add_courses(courses)
        # That functon is not yet implemented.

    # noinspection PyIncorrectDocstring
    def obs_addcourse(self, course, dept_abbrev, dept_name):
        """Adds a regblocks xml to the stated department.
        If the department is not present, adds it.
        Obsolete."""
        self.departments.setdefault(dept_abbrev, Dept(dept_abbrev, dept_name))
        self.departments[dept_abbrev].semiobs_add_course(course)

    # noinspection PyIncorrectDocstring
    def obs_convert_rb_json(self, json, *, islabs=False):
        """Converts a regblocks json to xml and adds the course.
        Obsolete."""
        s1 = json["sections"][0]
        dept_abbrev = s1["subject"]
        dept_name = s1["department"]
        course = parser.parse_course(json, islabs=islabs)
        self.obs_addcourse(course, dept_abbrev, dept_name)

    # noinspection PyIncorrectDocstring
    def obs_convert_list_of_rb_jsons(self, jsonlist):
        """Adds each course in a list of regblocks jsons.
        Obsolete."""
        for json in jsonlist:
            self.obs_convert_rb_json(json)
            self.obs_convert_rb_json(json, islabs=True)
