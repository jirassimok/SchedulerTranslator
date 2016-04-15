""" schedjson.py

Author: Jacob Komissar

Date: 2016-04-10

Self-parsing schedb classes file.

Temporarily put on hold to complete the lesser version of the functions in time
for course registration.

"""
# from ..fetch import Fetch


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

