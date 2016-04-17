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
        # Known possible values: Lecture, Lab, Conference

        professor = instructor["name"]
        professor_email = instructor["email"]  # May be None
        self.professor = professor.split(",")[0] # Last name only*
        self.professor_sort_name = professor
        if professor == "Not Assigned":
            self.professor_email = "N/A"
        elif professor_email:
            self.professor_email = professor_email
        else:
            self.professor_email = "look@it.up"

        # TODO: Concatenating CRN to room number isn't the best solution, but...
        # it's the best I've got right now.
        location  = meeting["location"].split(" ") + ([str(crn)] if crn else [])
        self.building = location[0]
        self.room = ((" ".join(location[1:]) if location[2:] else "[ERROR]"))
        # The test uses [2:] because attaching the crn nearly guarantees [1:]

        days = meeting["daysRaw"]
        self.days = self.fix_days(meeting["daysRaw"])
        self.starts = self.fix_time(meeting["startTime"], default="8:00AM")
        self.ends = self.fix_time(meeting["endTime"], default="4:50PM")

        # * The new scheduler uses the same value for instructor id and name
        #   And id might not be a sort name, anyway. But maybe...
        # TODO: Possibly use instructor["id"] for professor_sort_name

    def __str__(self):
        return ('<period type="' + self.type + '" professor="' + self.professor
                + '" professor_sort_name="' + self.professor_sort_name
                + '" professor_email="' + self.professor_email + '" days="'
                + self.days + '" starts="' + self.starts + '" ends="'
                + self.ends + '" building="' + self.building + '" room="'
                + self.room + '"></period>')

    def fix_days(self, raw_days):
        """ Parse a list of days in the format "MTWRF" into the format
        "mon,tue,wed,thu,fri".

        @param raw_days: A string of single-letter day abbreviations.
        @return: A string of comma-separated three-letter day abbreviations.
        """
        timetable = {'M': 'mon', 'T': 'tue', 'W': 'wed', 'R': 'thu', 'F': 'fri'}
        days = []
        for day in raw_days:
            days.append(timetable[day])
        return ','.join(days)

    def fix_time(self, time, *, default="12:00PM"):
        """ Parse a time in "%H%M" format to "%I:%M%p" format.

        Examples:
         930 ->  "9:30AM"
        2200 -> "10:00PM"

        @param time: An integer representation of a time in 24-hour format.
        @param default: The value to use in the event of an error.
        @return: A formatted time string.
        """
        try:
            return strftime("%I:%M%p", strptime(str(time), "%H%M")).lstrip("0")
        except ValueError:  # time didn't match format string
            self.professor += "[ERROR: Bad time]"
            return default
        # Potential bug: classes starting after 4:50 with invalid end times will
        # end before they begin.
