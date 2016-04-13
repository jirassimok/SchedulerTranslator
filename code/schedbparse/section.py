""" section.py

Author: Jacob Komissar

Date: 2016-04-12

Class to represent sections.

This class is created by and popualtes Course objects, and creates and populates
itself with Period objects.

Style note:
Where the schedb xml uses hyphens in attribute names, I use camelCase for the
matching
"""
from schedbparse.period import Period

class Section(object):
    def __init__(self):
        self.numberlist = []  # Will store e.g. A01 for all subsections
        self.number = None  # Will store e.g. "A01 X02"
        self.periods = []

    def add_main_info(self, jsection):
        print("SECTION DATA FOR", jsection["id"])

    def fix_section_number(self):
        """ Concatenate lab and section numbers.
        Probably should be part of or called from add_period. """
        self.number =  ' '.join((num[1:] if len(num)>3 else num)
                                for num in self.numberlist)


    def add_meetings(self, jsection):
        """ Parsess a regblocks section into one or more periods and adds them
         to this Section.
         """
        # TODO: This should loop over jsection["meetings"] and build a bunch of periods,
        # much like Course.add_regblocks, and populate this.
        period = Period('1','2','3','4','5','6','7','8')

        self.numberlist.append(jsection["sectionNumber"])
        self.numberlist.sort()
        # I wanted to use bisect.insort for those last two steps, but there is
        # no need to optimize insertion for a list that will only rarely have
        # more than two elements.
