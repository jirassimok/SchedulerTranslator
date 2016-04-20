""" section.py

Author: Jacob Komissar

Date: 2016-04-12

Class to represent sections.

This class is created by and popualtes Course objects, and creates and populates
itself with Period objects.

The Section class parses regblocks jsons' section portions, which it must be
passed separately.

Style note:
Where the schedb xml uses hyphens in attribute names, I use camelCase for the
matching variables here.
"""
from .period import Period


class Section(object):
    def __init__(self, jsection=None):
        # Composite info
        self.numberlist = []  # Will store e.g. A01 for all subsections
        self.number = None  # Will store e.g. "A01 X02"
        self.periods = []

        self.crn = None
        self.term = None  # YEAR[SEMESTER]
        self.partOfTerm = None  # X term
        self.seats = None
        self.availableseats = None
        self.max_waitlist = None
        self.actual_waitlist = None

        if jsection:
            self.add_main_info(jsection)
            self.add_meetings(jsection)

    def __eq__(self, other):
        """ Sections are equal if they have the same section numbers.
        Please do not compare sections from different courses. That's dumb.
        """
        return type(self) is type(other) and self.number == other.number

    def __lt__(self, other):
        """ A section is less than another if its number is lower.
        @raise TypeError if other is not a Section.
        """
        if isinstance(other, Section):
            return self.number < other.number
        else:
            return not self > other  # bad shortcut to unorderable TypeError

    def __str__(self):
        string = ['<section crn="', self.crn, '" number="', self.number,
                  '" seats="', self.seats, '" availableseats="',
                  self.availableseats, '" max_waitlist="', self.max_waitlist,
                  '" actual_waitlist="', self.actual_waitlist, '" term="',
                  self.term, '" part-of-term="', self.partOfTerm, '">']
        for p in self.periods:
            string.append(str(p))
        string.append('</section>')
        stringlist = [str(s) for s in string]
        return ''.join(stringlist)

    def is_valid(self):
        """ True if all attributes are truthy. """
        return all(self.__dict__.values())

    @staticmethod
    def fix_term(parts_of_term):
        """ Parse a string of the form "Season YEAR - X Term" into a string
        of the form "YEARSM" and a string of the form "X Term", where SM is the
        semester's number.

        @param parts_of_term: The string to parse.
        @return: A tuple of the semester number/string and term strings.
        """
        split = parts_of_term.split(' - ')  # ["Season YEAR", "X Term"]
        semester = split[0].split()  # ["Season", "YEAR"]
        semesters = {"Fall": "01", "Spring": "02"}  # , "Summer": "03"
        try:
            semesternum = semesters[semester[0]]
            semesterstring = semester[1] + semesternum  # YEARSM
        except KeyError:
            raise KeyError("Invalid part of term: " + str(semester[0]))
        if split[1] == "Full Semester":
            semesters = {"01": "A Term, B Term", "02": "C Term, D Term"}
            split[1] = semesters[semesternum]
        return semesterstring, split[1]

    def fix_section_number(self):
        """ Concatenate lab and section numbers.
        Probably should be part of or called from add_meetings. """
        self.numberlist.sort()  # should always be sorted anyway
        self.number = ' '.join((num[1:] if len(num) > 3 else num)
                               for num in self.numberlist)

    def add_main_info(self, jsection):
        """ Fill out universal data in the section, which should be shared by
        all of this object's periods.

        @param jsection: The section json to read data from.
        """
        termtuple = self.fix_term(jsection["partsOfTerm"])
        self.term = termtuple[0]
        self.partOfTerm = termtuple[1]
        self.crn = jsection["id"]
        # TODO Possibly switch to use crn from lab period - but which if more?
        # TODO VERY IMPORTANT: Find a way to store lab/conference CRNs. Issues:
        # We could use the lab period CRN, which would work because we have the
        # lectures also listed as seaprate courses, but this approach would fail
        # for courses with both a lab and a conference, because those have 3
        # CRNs, and we can only easily store one per period.
        # The second option is to concatenate them WITHOUT SPACES to the main
        # CRN. This would work all right, but would be a pain to read.

        # print("SECTION DATA FOR", jsection["id"])

    def add_meetings(self, jsection):
        """ Parse a regblocks section into one or more periods and add them to
        this Section.

        Any values not fully parsed/handled here are handled/parsed by
        Period.fix_values, and are marked here with "# *raw" and a reason.

        @param jsection: The json regblocks["section"] to parse and add.
        """

        # Get information shared by all periods.
        crn = jsection["id"]
        _type = jsection["component"]
        # note: Only the first listed instructor will be included.
        instructor = jsection["instructor"][0]
        for meeting in jsection["meetings"]:
            period = Period(_type, instructor, meeting, crn)
            if not period.days:
                period.days = "wed"
            self.periods.append(period)

        # print("PERIOD", jsection["sectionNumber"])

        self.numberlist.append(jsection["sectionNumber"])
        self.numberlist.sort()
        self.fix_section_number()
        # TODO: This should modify more of own properties.
        # So far, this properly constructs a period. It still needs to update
        # this section's (available)seats and waitlists.

        # Use the seats from the smallest subsection.
        seats = jsection["seatsCapacity"]
        if not self.seats or seats < self.seats:
            self.seats = str(jsection["seatsCapacity"])
            self.availableseats = str(jsection["openSeats"])
            self.max_waitlist = str(jsection["waitlist"])
            self.actual_waitlist = str(jsection["waitlistOpen"])
