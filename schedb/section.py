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
import re # for dealing with section numbers


class Section(object):
    def __init__(self, jsections):
        # Composite info
        self.numberlist = []  # Will store e.g. A01 for all subsections
        self.number = None  # Will store e.g. "A01 X02"
        self.periods = []

        termtuple = self.fix_term(jsections[0]["partsOfTerm"])
        self.term = termtuple[0]  # YEAR[SEMESTER]
        self.partOfTerm = termtuple[1] # X term

        self.crn = jsections[0]["id"]
        self.seats = None
        self.availableseats = None
        self.max_waitlist = None
        self.actual_waitlist = None

        for jsection in jsections: # Add meetings for all sections
            self.add_meetings(jsection)
        self.fix_section_number()

    def __eq__(self, other):
        """ Sections are equal if they have the same section numbers.
        Please do not compare sections from different courses. That's dumb.
        """
        return type(self) is type(other) and self.number == other.number

    def __lt__(self, other):
        """ A section is less than another if its number is lower.
        @raise TypeError if other is not a Section.
        """
        if isinstance(other, Section) and other.number is not None and self.number is not None:
            return self.number < other.number
        elif isinstance(other, Section):
            raise AttributeError("Sections without numbers are unorderable.")
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

        Called from add_meetings and the optional init.
        The rules for creating full section numbers are as follows:

        If any of the section's numbers beings with an A, B, C, or D followed by
        two digits, that number becomes the main number. Numbers with no additional
        characters are prioritized in this selection.

        If a main number is found and all of the numbers begin with the same
        character, that character will be removed from the beginning of every
        number besides the main number.

        The main number is placed before the other numbers, which are organized
        alphabetically.

        If no main number is found or the numbers begin with different characters,
        the numbers will be placed in alphabetical order.
        """
        self.numberlist.sort()  # should always be sorted anyway
        # obsolete version, replaces everything below it
        #self.number = ' '.join((num[1:] if len(num) > 3 else num)
        #                       for num in self.numberlist)
        for number in self.numberlist:
            if re.match(r'^[ABCD][0-9][0-9]$', number):
                break
        else:  # if no ideal main number was found, try numbers with extra ends
            for number in self.numberlist:
                if re.match(r'^[ABCD][0-9][0-9]', number):
                    break
            else:
                number = None

        # if a main section was determined and all numbers start with the same letter
        if number and all((num.startswith(number[0]) for num in self.numberlist)):
            # put the main section at the start and remove the first letter of each other section
            self.numberlist = [num[(1 if len(num)>3 else 0):] for num in self.numberlist if (not (num == number))]
            self.numberlist.insert(0, number)

        self.number = ' '.join(self.numberlist)

        """
        To deal with unusual section numbers, follow these rules;
        Section number [ABCD][0-9][0-9] is assumed to be the main section if present.
        Otherwise, a section starting with that pattern is the main secction, if present.
        Otherwise, all sections are presented in alphabetical order.

        If a main section is present, all other sections have the first letter of that section removed from their number,
        unless only some can, in which case none do.


        If exactly one main number is present,
            Use it.
        If multiple main numbers are present,
            Use all numbers directly.
        If no main numbers are present,
            If a near-main number is present...
            If multiple...
            If no near-main numbers are present,
                Use all numbers directly.


        """

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
        # TODO: This should modify more of own properties.
        # So far, this properly constructs a period. It still needs to update
        # this section's (available)seats and waitlists.

        # Use the seats from the smallest subsection.
        # TODO: IMPORTANT. Deal with classes with both a lab and a conference.
        # Possibly track sizes of both by padding to longer size and concatenating as strings.
        seats = jsection["seatsCapacity"]
        if not self.seats or seats < self.seats:
            self.seats = str(jsection["seatsCapacity"])
            self.availableseats = str(jsection["openSeats"])
            self.max_waitlist = str(jsection["waitlist"])
            self.actual_waitlist = str(jsection["waitlistOpen"])
