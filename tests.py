#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import sys
import os
from schedb import schedb, department, course, section, period

class DeptTests(unittest.TestCase):
    def test(self):
        pass

class CourseTests(unittest.TestCase):
    def setUp(self):
        self.c = course.Course(999, "testCourse",
                          desc="this is a test", minCredits=1,
                          maxCredits=1, gradeType="normal", dept=None)
    def testToString(self):
        self.assertEqual(str(self.c), '<course number="999" name="testCourse"'
                         ' course_desc="this is a test" min-credits="1"'
                         ' max-credits="1" grade-type="normal"></course>')

    def testRegblocks(self):
        regblocksjson = {"registrationBlocks": [{"sectionIds": ["TestA"]}],
                         "sections": [{"id": "TestA", "description": "this is a test"}]}
        with patch('schedb.course.Section',
                   **{"return_value.__str__.return_value": "<mock_section />"}) as mock_section:
            self.c.add_regblocks(regblocksjson)
            self.assertEqual(str(self.c), '<course number="999"'
                             ' name="testCourse" course_desc="this is a test"'
                             ' min-credits="1" max-credits="1"'
                             ' grade-type="normal"><mock_section /></course>')
            mock_section.assert_called_once_with([{'id': 'TestA', 'description': 'this is a test'}])

class SectionTests(unittest.TestCase):
    def testToString(self):
        jsections = [{'partsOfTerm': 'Fall 2016 - A Term',
                      'instructor': ['testA'],
                      'id': '12345',
                      'component': 'lecture',
                      'meetings': ["testB"],
                      'openSeats': 25,
                      'waitlistOpen': '19',
                      'sectionNumber': 'A01',
                      'waitlist': '1',
                      'seatsCapacity': '144'}]
        with patch('schedb.section.Period',
                   **{"return_value.__str__.return_value": "<mock_period />"}) as mock_period:
            s = section.Section(jsections)
            self.assertEqual(str(s), '<section crn="12345" number="A01"'
                             ' seats="144" availableseats="25" max_waitlist="20"'
                             ' actual_waitlist="19" term="201601"'
                             ' part-of-term="A Term"><mock_period /></section>')
            mock_period.assert_called_once_with('lecture', "testA", "testB", '12345')

    def testMinSeats(self):
        jsections = [{'partsOfTerm': 'Fall 2016 - A Term',
                      'instructor': ['testA'],
                      'id': '12345',
                      'component': 'lecture',
                      'meetings': ["testB"],
                      'openSeats': 25,
                      'waitlistOpen': '19',
                      'sectionNumber': 'A01',
                      'waitlist': '1',
                      'seatsCapacity': '144'},
                     {'partsOfTerm': 'Fall 2016 - A Term',
                      'instructor': ['testC'],
                      'id': '12346',
                      'component': 'lecture',
                      'meetings': ["testD"],
                      'openSeats': 2,
                      'waitlistOpen': '1',
                      'sectionNumber': 'X01',
                      'waitlist': '0',
                      'seatsCapacity': '2'}]
        with patch('schedb.section.Period',
                   **{"return_value.__str__.return_value": "<mock_period />"}) as mock_period:
            s = section.Section(jsections)
            self.assertEqual(str(s), '<section crn="12345" number="A01 X01"'
                             ' seats="2" availableseats="2" max_waitlist="1"'
                             ' actual_waitlist="1" term="201601"'
                             ' part-of-term="A Term">'
                             '<mock_period /><mock_period /></section>')
            calls = [unittest.mock.call('lecture', "testA", "testB", '12345'),
                     unittest.mock.call('lecture', "testC", "testD", '12346')]
            mock_period.assert_has_calls(calls)

class PeriodTests(unittest.TestCase):
    def testToString(self):
        instructor = {"name": "TestB",
                      "email": "testC@test.com"}
        meeting = {"location": "TestC TestD",
                   "daysRaw": "MTRF",
                   "startTime": "0300",
                   "endTime": "0500"}
        p = period.Period("TestA", instructor, meeting, crn='12345')
        self.assertEqual(str(p), '<period type="TestA" professor="TestB"'
                         ' professor_sort_name="TestB"'
                         ' professor_email="testC@test.com"'
                         ' days="mon,tue,thu,fri" starts="3:00AM" ends="5:00AM"'
                         ' building="TestC" room="TestD 12345"></period>')

if __name__ == "__main__":
    unittest.main()
