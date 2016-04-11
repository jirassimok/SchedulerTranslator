""" parser.py

Author: Jacob Komissar

Date: 2016-04-10

Original json to schedb parsing functions.

These functions should be replaced by methods of the schedb classes.

"""
from .dept import Dept
from .coursec import *


class ParseError(Exception):
    pass


# noinspection PyIncorrectDocstring
def parse_periods(section):
    """Parses a section json into a list of Periods."""
    # TODO: Replace the errstring with something better, like skipping the class.
    errstring = [""]  # Will be included if bad things happen.
    def convert_time(tnum, *, errstring=[]):
        # converts time in min-digit 24-hr int format to 12-hr "H:MMPA" format
        try:
            return strftime("%I:%M%p", strptime(str(tnum), "%H%M")).lstrip("0")
        except ValueError:
            errstring[0] += "ERROR invalid meeting time "
            return "00:00AM"
    prof = section["instructor"][0]["name"]  # not gonna bother with this
    Type = section["component"]
    timetable = (("M", "mon"), ("T", "tue"), ("W", "wed"),
                 ("R", "thu"), ("F", "fri"))
    periods = []
    for met in section["meetings"]:
        rawdays = met["daysRaw"]
        days = ""
        for d in timetable:
            if d[0] in rawdays:
                days += d[1] + ","
        days = days.rstrip(",")
        if not days:
            days = "wed"
            errstring[0] += "ERROR no days listed "
        starts = convert_time(met["startTime"], errstring=errstring)
        ends = convert_time(met["endTime"], errstring=errstring)
        split = met["location"].split()
        if split:
            building = split[0]
            room = split[-1]
        else:
            building = "X"
            room = "X"
            errstring[0] += "ERROR bad location "
        if errstring:
            prof = errstring[0]
        periods.append(Period(Type, prof, days, starts, ends, building, room))
    return periods


# noinspection PyIncorrectDocstring
def parse_section(sec):
    """ Reads a section json, and returns a Section object representing it.
    Currently, lab/conference sections return False instead.

    :return Section or False
    """
    def parse_term(termstring):
        ts = termstring.split(' - ')
        TL = ts[0].split()  # ["Season", "YEAR"]
        termnum = TL[1]
        if TL[0] == "Fall":
            termnum += "01"
        elif TL[0] == "Spring":
            termnum += "02"
        elif TL[0] == "Summer":
            termnum += "03"
        else:
            raise ParseError("Invalid part of term: " + str(TL[0]))
        return termnum, ts[1]

    number = sec["sectionNumber"]
    if "X" in number:
        return False  # skip lab/conference sections
    crn = sec["registrationNumber"]
    seats = sec["seatsCapacity"]
    availableseats = str(sec["openSeats"])  # also see sec["seatsFilled"]
    max_waitlist = sec["waitlist"]  # always 0? for 1101
    actual_waitlist = sec["waitlistOpen"]  # also always 0? for CS1101
    term = parse_term(sec["partsOfTerm"])[0]
    partOfTerm = parse_term(sec["partsOfTerm"])[1]
    section = Section(crn, number, seats, availableseats, max_waitlist,
                      actual_waitlist, term, partOfTerm)
    section.periods = parse_periods(sec)
    return section


# noinspection PyIncorrectDocstring
def parse_course(json):
    """ Reads a course json, adding the couse to self.

    Bugs/poor design: If the first section does not accurately represent the
            course, the course will not be built correctly.
    """
    # abbrev = json["registrationBlocks"][0]["id"].split(";;")[0]
    # number = json["registrationBlocks"][0]["id"].split(";;")[1].split("@")[0]
    s1 = json["sections"][0]
    # dept_abbrev = s1["subject"]
    # dept_name   = s1["department"]
    name = s1["title"]
    number = s1["course"]
    course_desc = s1["description"].replace('<br />', '')
    minCredits = s1["creditsMin"]
    maxCredits = s1["creditsMax"]
    course = Course(number, name, course_desc, minCredits, maxCredits)
    for s in json["sections"]:
        sec = parse_section(s)
        if sec:  # skip sections that parse_section rejects
            course.sections.append(sec)
    return course


# noinspection PyIncorrectDocstring
def singleton_dept(json):
    """ Very obsolete. Creates department with course.å """
    s1 = json["sections"][0]
    dept_abbrev = s1["subject"]
    dept_name = s1["department"]
    dept = Dept(dept_abbrev, dept_name)
    dept.courses.append(parse_course(json))
    return dept


'''
def sort_sections(json):
    """
    Takes a json section list, and returns a tuple in the format
    ([lectures], [labs/conferences]).
    """
    for section in json["sections"]:
        if "X" in section["sectionNumber"]:
            pass
'''
