""" period.py

Author: Jacob Komissar

Date: 2016-04-12

Class to represent periods.

This class' participation in the parsing process is limited to extracting its
own string data from a meeting json and reformatting some of the strings.

"Lab" refers to any non-central period of a course, including labs, conferences,
and any other

Style note:
Where the schedb xml uses hyphens in attribute names, I use camelCase for the
matching variables here.
"""
from time import strftime, strptime


class Period(object):
    def __init__(self, _type, instructor, meeting, crn=''):
        # List sub-crns next to portion of class.
        self.type = _type  # type can not be modified
        # Known possible values: Lecture, Lab, Conference, Web

        professor = instructor["name"]  # ["id"] also works
        professor_email = instructor["email"]  # May be None
        self.professor = professor.split(",")[0]  # Last name only*
        self.professor_sort_name = professor
        if professor == "Not Assigned":
            self.professor_email = "N/A"
        elif professor_email:
            self.professor_email = professor_email
        else:
            self.professor_email = "look@it.up"

        # TODO: Concatenating CRN to room number isn't the best solution, but...
        # it's the best I've got right now.
        location = meeting["location"].split(" ") + ([str(crn)] if crn else [])
        self.building = location[0]
        self.room = (" ".join(location[1:]) if location[2:] else "?")
        # The test uses [2:] because attaching the crn nearly guaranteses [1:]

        self.days = self.fix_days(meeting["daysRaw"])
        self.starts = self.fix_time(meeting["startTime"], default="7:50AM")
        self.ends = self.fix_time(meeting["endTime"], default="7:50AM")

        # DONE: Deal with missing information more elegantly, esp. in Period.
        # Poorly deal with missing information.
        if meeting["location"] is None:
            self.building = "?"
            self.room = str(crn) if crn else "?"

        if not meeting["daysRaw"]:
            self.days = "?"

    def __str__(self):
        return ('<period type="' + self.type + '" professor="' + self.professor
                + '" professor_sort_name="' + self.professor_sort_name
                + '" professor_email="' + self.professor_email + '" days="'
                + self.days + '" starts="' + self.starts + '" ends="'
                + self.ends + '" building="' + self.building + '" room="'
                + self.room + '"></period>')

    def fix_days(self, raw_days, default="wed"):
        """ Parse a list of days in the format "MTWRF" into the format
        "mon,tue,wed,thu,fri".

        @param raw_days: A string of single-letter day abbreviations.
        @return: A string of comma-separated three-letter day abbreviations.
        """
        timetable = {'M': 'mon', 'T': 'tue', 'W': 'wed', 'R': 'thu', 'F': 'fri'}
        days = []
        for day in raw_days:
            try:
                days.append(timetable[day])
            except KeyError:  # a nonsense day was in the json
                # self.professor += "[ERROR: bad day " + day + "]"
                pass
        return ','.join(days)

    def fix_time(self, time, *, default="12:00PM"):
        """ Parse a time in "%H%M" format to "%I:%M%p" format.

        The default should always be specified.

        Examples:
         930 ->  "9:30AM"
        2200 -> "10:00PM"
        31023-> "?"

        @param time: An integer representation of a time in 24-hour format.
        @param default: The value to use in the event of an error.
        @return: A formatted time string or "?".
        """
        try:
            return strftime("%I:%M%p", strptime(str(time), "%H%M")).lstrip("0")
        except ValueError:  # time didn't match format string
            # self.professor += " [ERROR: bad time " + str(time) + "]"
            return "?"
        # Potential bug: classes starting after 4:50 with invalid end times will
        # end before they begin.
