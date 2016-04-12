""" Translator.py

Author: Jacob Komissar

Date: 2016-04-10

Program to convert WPI Course Planner jsons into a WPI Scheduler schedb.

Version 3
    Adapting to work with json_fetcher.
    Improving object-orientism further.
    Moved global methods into Parser class.

This program is able to convert a json or list of jsons into an object that
    prints as a schedb.

Methods labelled "Obsolete" in their docstrings are leftover from before the
rewrite. They are still potentially useful, especially as templates for newer
functions.

Style notes:
In the classes below, camelcase is used where the schedb uses a dash to separate
    words.
Not all of this is documented.

Currently, jsonFetcher cleans the data before it is passed here.
This isn't the most object-oriented way to do things, but it works... for now.
"""
# from time import strftime, strptime

'''
INPUT_FILE = "../TranslatorInput.json"
OUTPUT_FILE = "../output/TranslatorOutput.schedb"
'''

"""For parsing json from strings."""
true = True
false = False
null = None


class Period(object):
    def __init__(self, Type=None, professor=None, days=None, starts=None,
                 ends=None, building=None, room=None):
        self.type = Type
        self.professor = professor.split(",")[0]
        self.professor_sort_name = professor
        self.professor_email = "look@it.up"
        self.days = days
        self.starts = starts
        self.ends = ends
        self.building = building
        self.room = room

    def __str__(self):
        return ('<period type="' + self.type + '" professor="' + self.professor
                + '" professor_sort_name="' + self.professor_sort_name
                + '" professor_email="' + self.professor_email + '" days="'
                + self.days + '" starts="' + self.starts + '" ends="'
                + self.ends + '" building="' + self.building + '" room="'
                + self.room + '"></period>')


class Section(object):
    def __init__(self, crn=None, number=None, seats=None, availableseats=None,
                 max_waitlist=None, actual_waitlist=None, term=None,
                 partOfTerm=None):
        self.crn = crn
        self.number = number  # A01 etc IMPORTANT
        self.seats = str(seats)
        self.availableseats = str(availableseats)
        self.max_waitlist = str(max_waitlist)
        self.actual_waitlist = str(actual_waitlist)
        self.term = term
        self.partOfTerm = partOfTerm
        self.periods = []

    def __str__(self):
        string = ('<section crn="' + self.crn + '" number="' + self.number
                  + '" seats="' + self.seats + '" availableseats="'
                  + self.availableseats + '" max_waitlist="' + self.max_waitlist
                  + '" actual_waitlist="' + self.actual_waitlist + '" term="'
                  + self.term + '" part-of-term="' + self.partOfTerm + '">')
        for p in self.periods:
            string += str(p)
        return string + '</section>'

    def __bool__(self):
        """Sections are true if they have a CRN."""
        return False if self.crn is None else True

    def __eq__(self, other):
        """Sections with the same CRN are equal."""
        return isinstance(other, Section) and self.crn == other.crn

    def __ne__(self, other):
        return not self.__eq__(other)

    def parse_self(self, jsonsection):
        """
        Reads a section json, and returns a Section object representing it.
        Currently, lab/conference sections return False instead.
        """
        def parse_term(termstring):
            ts = termstring.split(' - ')
            TL = ts[0].split()  # ["Season", "YEAR"]
            termnum = TL[1]
            if TL[0] == "Fall":
                termnum += "01"
            elif TL[0] == "Spring":
                termnum += "02"
            else:
                # TODO: fix invalid terms
                # raise ParseError("Invalid part of term: " + str(TL[0]))
                pass
            return termnum, ts[1]

        self.number = jsonsection["sectionNumber"]
        if 'X' in self.number:
            self.crn = jsonsection["registrationNumber"]
        self.seats = jsonsection["seatsCapacity"]
        self.availableseats = str(jsonsection["openSeats"])
        self.max_waitlist = jsonsection["waitlist"]
        self.actual_waitlist = jsonsection["waitlistOpen"]
        self.term = parse_term(jsonsection["partsOfTerm"])[0]
        self.partOfTerm = parse_term(jsonsection["partsOfTerm"])[1]


class Course(object):
    def __init__(self, number=None, name=None, course_desc=None,
                 minCredits=None, maxCredits=None, dept=None,
                 *, json=None, sections=None, islabs=False):
        if json:
            self.parse_self(json)
            if sections:
                pass
                #add_section_only_data
        elif sections:
            self.parse_self_from_sections(sections)
        else:
            self.number = number  # num in dept 9999
            self.name = ('LAB: ' if islabs else '') + name
            self.course_desc = course_desc
            self.minCredits = str(minCredits)
            self.maxCredits = str(maxCredits)
            self.gradeType = "normal"
            self.dept = dept  # not used for xml - identification only
            self.sections = []
            self.islabs = islabs  # True if the course only holds lab sections

    def __str__(self):
        string = ('<course number="' + self.number + '" name="' + self.name
                  + '" course_desc="' + self.course_desc + '" min-credits="'
                  + self.minCredits + '" max-credits="' + self.maxCredits
                  + '" grade-type="' + self.gradeType + '">')
        for s in self.sections:
            string += str(s)
        return string + '</course>'

    def __eq__(self, other):
        """Courses with the same department and number are equal."""
        return (isinstance(other, Course) and self.number == other.number and
                self.dept == other.dept)

    def __ne__(self, other):
        return not self.__eq__(other)

    def parse_self_from_sections(self, json):
        """ Reads a course's section json, filling own info accordingly.

        Bugs/poor design: If the first section does not accurately represent the
                course, the course will not be built correctly.
        """
        s1 = json["sections"][0]
        self.number = s1["course"]
        self.name = s1["title"]
        # removal of html linebreak should be performed by jsonFetcher
        self.course_desc = s1["description"]  # .replace('<br />', '')
        self.minCredits = s1["creditsMin"]
        self.maxCredits = s1["creditsMax"]
        self.dept = s1["subject"]

    def parse_self(self, json):
        """ Parses some information from a course json.
        The rest must be parsed from a section json.
        Called by kw-only-arg in __init__. Course(json=X)
        """
        self.number = json["number"]
        self.name = json["title"]
        self.course_desc = json["description"]
        # self.parse_self_from_sections(json)

    def parse_sections(self, json):
        """ Obsolete. """
        for jsonsection in json["sections"]:
            sec = Section()
            sec.parse_self(jsonsection)
            if sec:  # if the parsing worked (if the section got a crn)
                self.sections.append(sec)
