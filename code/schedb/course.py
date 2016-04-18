""" course.py

Author: Jacob Komissar

Date: 2016-04-12

Class to represent courses and parse course jsons.

The Course class parses regblocks jsons registrationBlocks values, and minimally
parses the sections values for the sole purpose of setting up appropriate
sections by combining sections according to the registrationBlocks.

Style note:
Where the schedb xml uses hyphens in attribute names, I use camelCase for the
matching variables here.
"""
from .section import Section


class Course(object):
    def __init__(self, number, name, desc="[NO DESCRIPTION GIVEN]",
                 minCredits=1, maxCredits=1, gradeType="normal", *, dept):
        self.dept = dept  # Not used for xml - __eq__ only; may be None
        self.number = str(number)  # should always be string anyway
        self.name = str(name)  # same, as above, but you never know...
        self.course_desc = desc
        self.minCredits = str(minCredits)
        self.maxCredits = str(maxCredits)
        self.gradeType = gradeType
        self.sections = []
        # TODO: Rewrite course constructor to parse a little of something.
        # But it doesn't have to, does it?

    def __eq__(self, other):
        """ Two courses are equal if they have the same number and department.
        """
        return type(self) is type(other) and self.number == other.number \
            and self.dept == other.dept

    def __str__(self):
        string = ['<course number="', self.number, '" name="', self.name,
                  '" course_desc="', self.course_desc, '" min-credits="',
                  self.minCredits, '" max-credits="', self.maxCredits,
                  '" grade-type="', self.gradeType, '">']
        for s in self.sections:
            string.append(str(s))
        string.append('</course>')
        stringlist = map(str, string)
        return ''.join(stringlist)

    ''' Probably unnecessary, as I can just do "in self.sections".
    # Has potential uses if I were to extend this project a bunch, though.
    def __contains__(self, item):
        """ A course contains its sections. """
        return item in self.sections
    '''

    def add_regblocks(self, regblocksjson):
        """ Parse a regblocks json's two subsections to allow construction
        of sections, add each section.

        This function and add_regblock do most of the heavy lifting for the
        actual parsing of the scheduler jsons to schedb format.

        The parsing of a regblock section would have been carried out in the
        Section class, but the fact that regblock sections alone do not carry
        enough information (as period information is also stored in regblock
        registrationBlocks) led this function to be placed here.

        @param regblocksjson: The already-loaded registration blocks json.
        """
        # Separate the top-level elements of the regblocksjson.
        regblocks = regblocksjson["registrationBlocks"]
        sections = regblocksjson["sections"]

        regblocks = [regblock["sectionIds"] for regblock in regblocks if
                     regblock["enabled"] == True]
        jsections = {section["id"]: section for section in sections}

        for regblock in regblocks:  # A regblock is a list of crns.
            self.add_section(regblock, jsections)
        self.sections.sort()  # put them in order - enabled by Section.__lt__()

    def add_section(self, crns, jsections):
        """ Parse a sections json and a list of CRNs into one of this course's
        sections and its periods.

        @param crns: A list of the crns in the section.
        @param jsections: The sections in the regblocks json.
        """
        new_section = Section()
        first_subsection = True
        for crn in crns:
            try:
                jsection = jsections[crn]  # section is a regblocks[section]
            except KeyError:
                raise KeyError("Missing section: " + crn)

            # if it's a lecture or missing any information
            if len(jsection["sectionNumber"]) == 3 or first_subsection:
                first_subsection = False
                new_section.add_main_info(jsection)  # add info to object
                main_section = Section(jsection)
                if main_section not in self.sections:
                    self.sections.append(main_section)
            new_section.add_meetings(jsection)

        # Concatenate lab and lecture section numbers
        # TODO: Check if the section is correctly-populated first.
        if not new_section.is_valid():
            new_section.add_main_info
        if new_section not in self.sections:  # prevent duplicate sections
            self.sections.append(new_section)
