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



Top-down bits:

Besides the things I say each thing can be given, they can also be given
anything required for something below them, so they can pass it on. Also, it may
be possible to initialize these with additional values, but such options are not
used in the current implementation.

The Schedb takes a term list, which it actually SHOULD be able to parse!
Schedb(termlist)

A Term takes its string, and can be given its department list, which it turns
into a dictionary of abbrevs and Depts.
Term(termstring, deptlistjson)

A Dept takes its name and abbrev, and can be given its course list, which it
turns into a dictionary of course numbers and courses.

A Course takes its (department,) name(,) and number, and can be given its
regblocks, which it parses into its sections.

A Section takes nothing, and can be given its regblocks, which it parses into
itself and its periods.
Section()
Section.add_main_info(regblocks["section"])
Section.add_meetings(regblocks["section"])

A Period takes all of its information and can be given nothing.
Period(_type, instructor, meeting, crn)


# TODO NOTE: Currently, I could build the database without courses, then ...
# get all the regblocks, and add courses by looking at their departments.
# This might allow me to more-easily use my current framework with the new one,
# especially after making the new framework for Schedbs/Terms/Depts, but that
# isn't really a goal I need to have.


Add a safeguard against '""' appearing in the json. Before using json.loads



Fetch-down bits:
1. Get terms
 2. Store terms
3. Loop over stored terms, getting depts
   4. Store depts in loop, and...
  5. Loop over depts, getting course lists
     6. Store courses with minimal info, and...
    7. Loop over courses, getting regblocks
      8. Store regblocks - nothing left to get
    .. End course loop
  .. End dept loop
.. End term llop



Important notes on sections:
    Section numbers should be stored in a list in each section.
    Either after each is added, or before printing, they should be sorted
        and joined with either an empty string or a single space.
