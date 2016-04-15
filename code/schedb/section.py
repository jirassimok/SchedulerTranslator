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
        # Composite info
        self.numberlist = []  # Will store e.g. A01 for all subsections
        self.number = None  # Will store e.g. "A01 X02"
        self.periods = []
        '''
        # Main info - get from main regblock
        self.term = term
        self.partOfTerm = partOfTerm


        self.seats = str(seats)  # Add from smallest regblock
        self.availableseats = str(availableseats)  # Add from same as above
        self.max_waitlist = str(max_waitlist)  # Add from Smallest regblock
        self.actual_waitlist = str(actual_waitlist)  # Add from same as above
        '''

    def add_main_info(self, jsection):
        print("SECTION DATA FOR", jsection["id"])

    def fix_section_number(self):
        """ Concatenate lab and section numbers.
        Probably should be part of or called from add_meetings. """
        self.number =  ' '.join((num[1:] if len(num)>3 else num)
                                for num in self.numberlist)


    def add_meetings(self, jsection):
        """ Parse a regblocks section into one or more periods and add them to
        this Section.

        Any values not fully parsed/handled here are handled/parsed by
        Period.fix_values, and are marked here with "# *raw" and a reason.
        """
        crn = jsection["id"]
        _type = jsection["component"]
        # Only the first listed instructor will be included.
        professor = jsection["instructor"][0]["name"]
        professor_email = jsection["instructor"][0]["email"]  # *raw may be None

        # TODO: This should loop over jsection["meetings"] and build a bunch of periods,
        # much like Course.add_regblocks, and populate this.periods
        """ get info universal to meetings """
        for meeting in jsection["meetings"]:
            # days, starts, and ends are all in the wrong formats
            days = meeting["daysRaw"]  # *raw
            starts = meeting["startTime"]  # *raw
            ends = meeting["endTime"]  # *raw

            location = meeting["location"]
            period = Period(_type, professor, professor_email, days,
                            starts, ends, location, crn)
            period.fix_values()

        # print("PERIOD", jsection["sectionNumber"])
        self.numberlist.append(jsection["sectionNumber"])
        self.numberlist.sort()
        # I wanted to use bisect.insort for those last two steps, but there is
        # no need to optimize insertion for a list that will only rarely have
        # more than two elements.
        # TODO: This should call fix_section_number and should determine sizes.
