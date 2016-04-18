""" department.py

Author: Jacob Komissar

Date: 2016-04-12

Class to represent departments.
"""
from .course import Course


class Dept(object):
    orderlist = ("BB", "BCB", "CH", "CS", "GE", "MA", "PH", "AE", "AREN", "BME",
                 "CE", "CHE", "ECE", "ES", "FP", "ME", "RBE", "AB", "CN", "GN",
                 "SP", "AR", "EN", "HI", "HU", "MU", "PY", "RE", "WR", "ECON",
                 "ENV", "GOV", "PSY", "SD", "SOC", "SS", "ACC", "BUS", "ETR",
                 "FIN", "MIS", "MKT", "OBC", "OIE", "AS", "DS", "FY", "ID",
                 "IMGD", "INTL", "ISE", "MFE", "ML", "MME", "MPE", "MTE", "NSE",
                 "PE", "SEME", "STS", "SYS")

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

    def __lt__(self, other):
        """ A department is less than another if its abbreviation is earlier in
        this list (stored as Dept.orderlist):

        BB, BCB, CH, CS, GE, MA, PH, AE, AREN, BME, CE, CHE, ECE, ES, FP, ME,
        RBE, AB, CN, GN, SP, AR, EN, HI, HU, MU, PY, RE, WR, ECON, ENV, GOV,
        PSY, SD, SOC, SS, ACC, BUS, ETR, FIN, MIS, MKT, OBC, OIE, AS, DS, FY, ID,
        IMGD, INTL, ISE, MFE, ML, MME, MPE, MTE, NSE, PE, SEME, STS, SYS

        Alternatively, sort Depts in Schedb.
        [self.depts[abbr] for abbr in order if self.depts.get(abbr) is not None]

        @raise TypeError if other is not a Dept.
        @raise ValueError if either Dept's abbrev is not in Dept.orderlist.
        """
        if isinstance(other, Dept):
            return self.abbrev < other.abbrev
            '''
            (Dept.orderlist.index(self.abbrev)
                < Dept.orderlist.index(other.abbrev))
            '''
        else:
            return not self > other  # bad shortcut to unorderable TypeError

    @staticmethod
    def get_order():
        return Dept.orderlist

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
