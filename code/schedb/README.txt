schedbparse

This module was intended to replace schedb in a cleaner, more object-oriented
fashion. However, due to time constraints, it has been put on hold.

schedb.py currently contains the skeletons of the classes that represent the
    database. These should not remain in one file.


Current plan: Still use the old schedb classes, but with new algorithms.


TODO: WEED OUT SUMMER CLASSES AT THE HIGHEST POSSIBLE LEVEL: Schedb


Top-down bits:

Besides the things I say each thing can be given, they can also be given
anything required for something below them, so they can pass it on. Also, it may
be possible to initialize these with additional values, but such options are not
used in the current implementation.

The Schedb takes a term list, which it actually SHOULD be able to parse!
Schedb(termlist)

A Term takes its string, and can be given its department list, which it turns
into a dictionary of abbrevs and Depts.
Term(termstring)
Term.add_depts(deptlistjson)

A Dept takes its name and abbrev, and can be given its course list, which it
turns into a dictionary of course numbers and courses.
Dept(name, abbrev)
Dept.add_courses(courselistjson)

A Course takes its (department,) name(,) and number, and can be given its
regblocks, which it parses into its sections.
Course(number, name)
Course.add_regblock(regblockjson)

A Section takes nothing, and can be given its regblocks, which it parses into
itself and its periods.
Section()
Section.add_main_info(regblocks["section"])
Section.add_meetings(regblocks["section"])

A Period takes all of its information and can be given nothing.
Period(_type, instructor, meeting, crn)


pager = Fetch(...)
schedb = Schedb(pager.get()) TODO Fetch.get can not get terms right now

for term in schedb.terms:
    schedb.add_depts(pager.get(term.string))
    for dept in term.depts:
        dept.add_courses(pager.get(term, dept.abbrev))
        for course in dept.courses:
            course.add_regblocks(pager.get(term, dept.abbrev, course.number))


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
