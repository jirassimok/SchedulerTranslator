""" period.py

Author: Jacob Komissar

Date: 2016-04-12

Class to represent periods.

This class participates minimally, in the parsing process, only changing the
format of a few strings passed to it.

"Lab" refers to any non-central period of a course, including labs, conferences,
and any other

Style note:
Where the schedb xml uses hyphens in attribute names, I use camelCase for the
matching
"""


class Period(object):
    def __init__(self, _type, professor, professor_email, days,
                 starts, ends, location, crn=''):
        # List sub-crns next to portion of class.
        self.type = _type + (' ' + crn if crn else '')
        self.professor = professor.split(",")[0]  # Last name only*
        self.professor_sort_name = professor
        self.professor_email = professor_email if professor_email else "look@it.up"
        self.days = days
        self.starts = starts
        self.ends = ends

        location  = location.split(" ")
        self.building = location[0]
        self.room = " ".join(location[1:]) if location[1:] else "[ERROR]"

        # * The new scheduler uses the same value for instructor id and name
        #   And id might not be a sort name, anyway. But maybe...
        # TODO: Possibly use instructor["id"] for professor_sort_name



    """ Possible alternative to Period constructor - feels like better object-
    orientism, but will be much harder to maintain if the data format changes
    significantly. And as I'm already extracting some of the data from the json
    in Section.add_meetings, I might as well extract the rest.

    In the next git commit, to be carried out immediately after this comment is
    complete, this version of __init__ will replace the current one.

    def __init__(self, _type, instructor, meeting, crn=''):
        self.type = _type + (" " + crn if crn else '')
        professor = instructor["name"]
        self.professor = professor.split(",")[0]
        self.professor_sort_name = professor
        prof_email = instructor["email"]
        self.professor_email = prof_email if prof_email else "look@it.up"
        location  = location.split(" ")
        self.building = location[0]
        self.room = " ".join(location[1:]) if location[1:] else "[ERROR]"

        self.days = ...
        self.starts = ...
        self.ends = ...
    """

    def __str__(self):
        return ('<period type="' + self.type + '" professor="' + self.professor
                + '" professor_sort_name="' + self.professor_sort_name
                + '" professor_email="' + self.professor_email + '" days="'
                + self.days + '" starts="' + self.starts + '" ends="'
                + self.ends + '" building="' + self.building + '" room="'
                + self.room + '"></period>')

    def fix_values(self):
        pass