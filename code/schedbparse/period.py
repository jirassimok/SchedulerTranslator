""" period.py

Author: Jacob Komissar

Date: 2016-04-12

Class to represent periods.

This class participates mini

"Lab" refers to any non-central period of a course, including labs, conferences,
and any other

Style note:
Where the schedb xml uses hyphens in attribute names, I use camelCase for the
matching
"""


class Period(object):
    def __init__(self, _type, professor, professor_email, days,
                 starts, ends, building, room, crn=""):
        self.type = _type + ' ' + crn  # List sub-crns next to portion of class.
        self.professor = professor.split(",")[0]  # Last name only
        self.professor_sort_name = professor
        self.professor_email = professor_email
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
