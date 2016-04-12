""" schedjson.py

Author: Jacob Komissar

Date: 2016-04-10

Self-parsing schedb classes file.

Temporarily put on hold to complete the lesser version of the functions in time
for course registration.

"""
from ..fetch import Fetch


class Schedjson(object):
    def __init__(self):
        self.terms = []  # List because nothing to index by.


class Term(object):
    """ Represents term jsons and stores subject jsons.
    """
    def __init__(self, termstring):
        self.termstring = termstring
        self.subjects = {}  # index by abbrev


class Subject(object):
    """ Represents contents of sections of subject jsons.
    Stores courses jsons.
    """
    def __init__(self, id, long):
        self.id = id
        self.long = long
        self.courses = {}  # index by course number


class Course(object):
    """ Represents contents of indices of course jsons.
    Stores regblocks jsons.
    """
    #TODO Should these build full regblocks or store the data to do so?
    def __init__(self, regblocks, number, title):
        self.regblocks = regblocks  # regblocks json as dict
        self.number = number
        self.title = title
        self.sections = []

    def parse_regblocks(self):
        pass




class Sections(object):
    """ Will store the full data for a single registration block.
    """
    def __init__(self):
        periods = []
        # self.crn = crn
        # self.number = number  # A01 etc IMPORTANT
        # self.seats = str(seats)
        # self.availableseats = str(availableseats)
        # self.max_waitlist = str(max_waitlist)
        # self.actual_waitlist = str(actual_waitlist)
        # self.term = term
        # self.partOfTerm = partOfTerm
        # self.periods = []
