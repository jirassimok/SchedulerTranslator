schedbparse

This module was intended to replace schedb in a cleaner, more object-oriented
fashion. However, due to time constraints, it has been put on hold.

schedb.py currently contains the skeletons of the classes that represent the
    database. These should not remain in one file.


Current plan: Still use the old schedb classes, but with new algorithms.

TODO: Add final steps: xml.ElementTree.tostring(xml.ElementTree.fromstring(str(schedb)))

Previously, departments were built from per-term department lists and strings
as they currently are.

Course listings are used to get regblocks, and nothing more.
    lesser priority: There should probably be a check for missing courses/regblocks.


Courses are inserted with a department and course number.
    regblocks["subject"]
    regblocks["id"]


I leave it up to the dept class or something above it to parse courses.


This all takes place inside a course, starting with a regblocks json.

def Course.add_regblocks(self, regblocks):

sections = regblocksjson["sections"]
regblocks = regblocksjson["registrationBlocks"]

# regblock crns in list format: ((crn, crn), (crn, crn))
regblocks = [[regblock["sectionIds"]] for regblock in regblocks if
            regblock["enabled"]==True]

# sections in dict keyed by crn (as str) (section["registrationNumber"] also works)
jsections = { section["id"]: section for section in sections }

for regblock in regblocks:
    sec = Section()
    for crn in regblock:
        jsection = jsections[crn]  # jsection is a regblocks json
        period = Period(jsection)  # Parse the jsection's meeting times (plural!)

        if len(jsection["sectionNumber"])==3:  # if it's a lecture
            self.add_info_from_secjson(jsection) # add course info (credits, mainly)
            sec.add_main_info(jsection)  # add section info to section

        sec.add_period(period)  # ??

    if sec.[valid section]:  # Section function, probably recurs to period function
        self.sections.append(sec)


Add a safeguard against '""' appearing in the json. Before using json.loads



Important notes on sections:
    Section numbers should be stored in a list in each section.
    Either after each is added, or before printing, they should be sorted
        and joined with either an empty string or a single space.
