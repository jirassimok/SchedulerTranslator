schedb

This package contains five files (besdies this one and __init__.py), each
containing a single class. Each class represents a level of the xml (schedb)
file that the WPI Scheduler uses: schedb, dept, course, secction, and period.

--------------------------------------------------------------------------------

Below are various notes from the creation of this package.
I'll remove them later.t


DONE marks previous to-do items.

Current plan: Still use the old schedb classes, but with new algorithms.


DONE: WEED OUT SUMMER CLASSES AT THE HIGHEST POSSIBLE LEVEL: Schedb


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

Too-basic version
pager = Fetch(...)
schedb = Schedb()
schedb.add_terms(pager.get_json())
for term in schedb.terms:
    schedb.add_depts(pager.get_json(term))
    for dept in term.depts:
        dept.add_courses(pager.get_json(term, dept.abbrev))
        for course in dept.courses:
            course.add_regblocks(pager.get_json(term, dept.abbrev, course.number))

DONE Likely code-breaking flaw: Loop will attempt to add all courses every term.
There is no problem at the point of getting nonexistant departments for any
given term, because the department loop is based in the term.
There may be a risk in adding courses, as the department's courses carry over
from the previous term.
Possible solution: give departments an additional list.
The best solution might be to try/except the 404 error pager.get{_json}() gives,
except that that could drastically increase the number of requests (but only for
the local database, if this is used properly).
Or look at the loop block below.

pager = Fetch(local=True)
schedb = Schedb(pager.get_json())  # initialize with terms

for term in schedb.terms:
    depts = pager.get_json(term)
    schedb.add_depts(depts)
    for deptjson in depts:
        dept = deptjson["id"]
        courselist = pager.get_json(term, dept)
        schedb.add_courses_to_dept(courselist, dept)
        for course in courselist:
            number = courselist["number"]
            regblocks = pager.get_json(term, dept["id"], number)
            schedb.add_regblocks(regblocks, dept, number)


# NOTE: Currently, I could build the database without courses, then ...
# get all the regblocks, and add courses by looking at their departments.
# This might allow me to more-easily use my current framework with the new one,
# especially after making the new framework for Schedbs/Terms/Depts, but that
# isn't really a goal I need to have.


Add a safeguard against '""' appearing in the json. Before using json.loads
Unecessary - that's still valid, and can be dealt with elsewhere.


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
