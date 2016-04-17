""" schedjson.py

Author: Jacob Komissar

Date: 2016-04-10

Self-parsing schedb classes file.

Temporarily put on hold to complete the lesser version of the functions in time
for course registration.

"""
from .department import Dept


class Schedb(object):
    def __init__(self):
        self.terms = []  # List because nothing to index by. - could be a set
        self.depts = {}

    def add_terms(self, json_terms):
        """ Add a list of terms to this schedb. Prevents addition of duplicates.

        @param json_terms: A term list json.
        """
        for term in json_terms:
            termstring = term["id"]  # could also use term["title"]
            if termstring not in self.terms:
                self.terms.append(termstring)

    def add_depts(self, json_dept_list):
        """ Add a list of departments to this schedb.

        @param json_dept_list: A department list json.
        """
        for dept in json_dept_list:
            abbrev = dept["id"]  # Could use short, but id is more likely unique
            self.depts.setdefault(abbrev, Dept(abbrev, dept["long"]))
