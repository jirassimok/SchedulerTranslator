""" testmain.py

For testing the schedb package.

Temporary version to act as main while I choose courses.
"""
from schedb.course import Course
from schedb.schedb import Schedb
from schedb.department import Dept
from schedb.period import Period
import json
from fetch import Fetch

DATABASE = "../DATABASE"

""" Course tests. """
def test_course():
    course = Course(1101, "Intro to CS", "Learn stuff.")
    true = True
    false = False
    null = None
    with open("testregblocks.json") as jsonfile:
        testrbs = json.load(jsonfile)
    course.add_regblocks(testrbs)
    # print(course)

    with open(DATABASE + "/terms/Fall 2016/subjects/CS/courses/1101/"
              "regblocks.json") as jsonfile:
        fullrbtest = json.load(jsonfile)
    course.add_regblocks(fullrbtest)
    print(course)

#test_course()


def test_schedb():
    """ Schedb term and department tests. """
    with open("../../DATABASE/terms.json") as jsonfile:
        schedb = Schedb(json.load(jsonfile))

    def add_term_depts(term):
        with open(DATABASE + "/terms/" + term + "/subjects.json") as jsonfile:
            schedb.add_depts(json.load(jsonfile))

    for a_term in schedb.terms:
        # if input("Enter anything to read term " + term + ".\n"):
        if a_term != "Spring 2016":
            add_term_depts(a_term)

    print("Departments:")
    for key in schedb.depts.keys():
        print(key)

#test_schedb()


""" Dept tests """


def test_dept():
    dept = Dept("CS", "Computer Science")

    def add_course_list(_term):
        with open("../../DATABASE/terms/" + _term + "/subjects/CS/courses.json"
                  ) as jsonfile:
            dept.add_courses(json.load(jsonfile))

    for term in {"Fall 2016", "Summer 2016", "Spring 2017"}:
        add_course_list(term)

    print("Courses:")
    for key in dept.courses.keys():
        print(key)

#test_dept()


pager = Fetch(local=True, port=8001)
schedb = Schedb(pager.get_json())  # initialize with terms
schedb.terms.remove("Spring 2016")


#'''
import sys
def print_now(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()

for term in schedb.terms:
    depts = pager.get_json(term)
    schedb.add_depts(depts)
    print_now("Term", term, "deptartments added.")
    for deptjson in depts:
        dept = deptjson["id"]
        courselist = pager.get_json(term, dept)
        schedb.add_courses_to_dept(courselist, dept)
        print_now("\tDept", dept, "courses added.")
        for course in courselist:
            number = course["number"]
            regblocks = pager.get_json(term, dept, number)
            schedb.add_regblocks(regblocks, dept, number)
            print_now("\t\t", dept, number, "processed.")
#'''

'''
""" Debugging Course, Section, and Period after Scheduler rejected the data. """
null = None
true = True
false = False
courses = [{"id":"MA|501","subject":"MATHEMATICAL SCIENCES","subjectShort":"MA","subjectId":"MA","number":"501","topic":null,"displayTitle":"501 MA ENGINEERING MATHEMATICS","title":"ENGINEERING MATHEMATICS","titleLong":"MATHEMATICAL SCIENCES 501 - ENGINEERING MATHEMATICS","description":null,"hasTopics":false}]

dept = Dept("MA", "Mathematical Sciences")
dept.add_courses(courses)

from pprint import pprint


dept.add_regblocks(pager.get_json("Fall 2016", "MA", "501"), "501")
a = dept.courses["501"].sections
for i in a:
    pprint(i.__dict__)
    for j in i.periods:
        pprint(j.__dict__)

print(dept)
'''
