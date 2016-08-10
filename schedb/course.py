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
        stringlist = [str(s) for s in string]
        return ''.join(stringlist)

    ''' Probably unnecessary, as I can just do "in self.sections".
    # Has potential uses if I were to extend this project a bunch, though.
    def __contains__(self, item):
        """ A course contains its sections. """
        return item in self.sections
    '''

    def add_regblocks(self, regblocksjson):
        """ Parse a regblocks json's two subsections to allow construction
        of sections, and add each section.

        This function and add_regblock do the heaviest lifting for the
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

        # filter removed because full courses are disabled
        regblocks = [regblock["sectionIds"] for regblock in regblocks]
                    # if regblock["enabled"] == True]
        jsections = {section["id"]: section for section in sections}

        for regblock in regblocks:  # A regblock is a list of crns.
            self.add_section(regblock, jsections)
        self.sections.sort()  # put them in order - enabled by Section.__lt__()

        self.course_desc = sections[0]["description"]

    def add_section(self, crns, jsections):
        """ Parse a sections json and a list of CRNs into one of this course's
        sections and its periods.

        @param crns: A list of the crns in the section.
        @param jsections: The sections in the regblocks json.
        """
        new_section = Section()
        for crn in crns:
            try:
                jsection = jsections[crn]  # section is a regblocks[section]
            except KeyError:
                raise KeyError("Missing section: " + crn)

            # if it's a lecture or missing any information
            if len(jsection["sectionNumber"]) == 3 or jsection["component"] == "Lecture":
                # TODO: Find a better way to identify the main section.
                # Possibilities:
                #   use jsection["component"]=="Lecture"
                # TODO: (maybe done) Fix bug causing incorrect information for main sections.
                # Could split main section and add_main_info
                new_section.add_main_info(jsection)  # add info to object
                main_section = Section(jsection)
                """ Might be better for consistency:
                main_section = Section()
                main_section.add_main_info(jsection)
                main_section.add_meetings(jsection)
                # and remove option to create Sections with jsection args,
                # but see alternative forms, below
                """
                if main_section not in self.sections:
                    self.sections.append(main_section)
            new_section.add_meetings(jsection)

        # Check if the section is correctly-populated first.
        # TODO: this should cause a warning or error of some sort,
        # rather than adding main info, because that might not be the problem.
        if not new_section.is_valid():
            new_section.add_main_info(jsections[crns[0]])

        new_section.fix_section_number()
        if new_section not in self.sections:  # prevent duplicate sections
            self.sections.append(new_section)

        # TODO: Consider the alternative forms.
        """ ALTERNATIVE FORMS
        1 would improve object-orientism, but would make identifying the main
        section more difficult.

        1.
        Possible alternative form for add_section, using an expanded Section
        initializer that parses a list of json sections:

        relevant_sections = []
        for crn in crns:
            try:
                relevant_sections.append(jsections[crn])
            except KeyError:
                raise KeyError("Missing section: " + crn)
        new_section = Section(relevant_sections)

        ... check validity ...
        ... add new secction to self.sections if not present ...

        2.
        This would have to be accompanied by updates to both Section.__init__
        and Course.add_regblocks.
        Section.__init__ would have to loop over the given jsections and add
        meetings. This would be a trivial change.

        There would have to be another way to find the main sections.

        I think the best way might be to use Course.add_regblocks to loop over
        the list of regblock CRNs and counting occurences of each CRN.
        Then they can be sorted into a number of groups equal to the number of
        CRNs in each regblock, where all regblocks contain one CRN from each
        group. From there, the main section may be identifiable.

        This is much easier to do without implementing alternative form 1,
        because Course.add_section can be used to return useful information for
        identifying the main section.
        """
