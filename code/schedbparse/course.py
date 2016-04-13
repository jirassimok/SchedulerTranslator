""" course.py

Author: Jacob Komissar

Date: 2016-04-12

Class to represent courses and parse course jsons.

Style note:
Where the schedb xml uses hyphens in attribute names, I use camelCase for the
matching
"""
from schedbparse.section import Section

class Course(object):
    def __init__(self, dept, number, course_desc="NO DESCRIPTION AVAILABLE",
                 minCredits=1, maxCredits=1, gradeType="normal"):
        self.dept = dept  # Not used for xml - identification only.
        self.number = number
        self.course_desc = course_desc
        self.minCredits = int(minCredits)
        self.maxCredits = int(maxCredits)
        self.gradeType = gradeType
        self.sections = []

    def __eq__(self, other):
        """ Two courses are equal if they have the same number and department.
        @param other: The object to compare to.
        """
        try:
            return self.number == other.number and self.dept == other.dept
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_regblocks(self, regblocksjson):
        """ Parses a regblocks json into this courses' sections and their
        periods.

        This function does most of the heavy lifting for the actual parsing
        of the scheduler jsons to schedb format.

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
        jsections = { section["id"]: section for section in sections }

        for regblock in regblocks:  # A regblock is a list of crns.
            new_section = Section()
            for crn in regblock:
                jsection = jsections[crn]  # section is a regblocks[section]
                if len(jsection["sectionNumber"])==3:  # if it's a lecture,
                    new_section.add_main_info(jsection)  # add info to object
                new_section.add_meetings(jsection)

            # Concatenate lab and lecture section numbers
            # Maybe check if the section is correctly-populated first?
            self.sections.append(new_section)






a = Course(1, 1)
true = True
false = False
null = None
testrbs = {"registrationBlocks":[     {"id":"CS;;1101@10290-15460",
         "sectionIds":[            "10290",
            "15460"],
         "optionalSectionIds":[],
         "selected":true,
         "locked":false,
         "showLock":false,
         "enabled":true,
         "disabledReasons":null,
         "desiredCourseId":null,
         "lcId":null},
     {"id":"CS;;1101@10290-10340",
         "sectionIds":[            "10290",
            "10340"],
         "optionalSectionIds":[],
         "selected":true,
         "locked":false,
         "showLock":false,
         "enabled":true,
         "disabledReasons":null,
         "desiredCourseId":null,
         "lcId":null},
     {"id":"CS;;1101@10344-15460",
         "sectionIds":[            "10344",
            "15460"],
         "optionalSectionIds":[],
         "selected":true,
         "locked":false,
         "showLock":false,
         "enabled":true,
         "disabledReasons":null,
         "desiredCourseId":null,
         "lcId":null}],
   "sections":[     {"optional":false,
         "registrationClosed":false,
         "courseAttributes":null,
         "credits":"3",
         "creditsMin":3.0,
         "creditsMax":3.0,
         "openSeats":95,
         "meetings":[           {"days":"MTThF",
               "daysRaw":"MTRF",
               "startTime":900,
               "endTime":950,
               "location":"FL PH-UPR",
               "meetingType":"CLAS",
               "startDate":"2016-08-25T00:00:00Z",
               "endDate":"2016-10-13T00:00:00Z",
               "mapURL":null,
               "firstMonday":"2016-08-22T00:00:00Z",
               "lastMonday":"2016-10-10T00:00:00Z"}],
         "academicCareer":"Graduate, High School (Mass Academy), Undergraduate",
         "academicCareerDescr":"Graduate, High School (Mass Academy), Undergraduate",
         "academicCareerDescrShort":"Graduate, High School (Mass Academy), Undergraduate",
         "campus":"Main",
         "campusShort":null,
         "classAssociations":null,
         "campusCode":"1",
         "campusDescription":"Main",
         "component":"Lecture",
         "corequisiteSections":[],
         "course":"1101",
         "customData":"",
         "department":"Computer Science",
         "description":"This course introduces principles of computation and programming with an emphasis on program design. Topics include the design, implementation and testing of programs that use a variety of data structures (such as structures, lists, and trees), functions, conditionals, recursion and higher-­‐order functions. Students will be expected to design simple data models, and implement and debug programs in a functional programming language. <br />     Recommended background: none. <br />Either CS 1101 or CS 1102 provides sufficient background for further courses in the CS department. Undergraduate credit may not be earned for both this course and CS 1102. <br />",
         "disabledReasons":[],
         "enrollmentStatus":null,
         "enrollmentRequirements":[],
         "exams":[],
         "fees":"",
         "freeFormTopics":null,
         "hasCorequisites":false,
         "hasSectionNotes":false,
         "hasPrerequisites":false,
         "id":"10290",
         "isHonors":false,
         "isWritingEnhanced":false,
         "location":null,
         "lrnComTitle":null,
         "notes":"",
         "partsOfTerm":"Fall 2016 - A Term",
         "prerequisites":"",
         "corequisites":"",
         "registrationNumber":"10290",
         "registrationType":null,
         "reserveCaps":[],
         "sectionAttributes":[],
         "sectionNumber":"A01",
         "sectionStatus":"Active",
         "subject":"CS",
         "subjectId":null,
         "title":"INTRO TO PROGRAM DESIGN",
         "topicId":null,
         "topicTitle":null,
         "waitlist":"0",
         "waitlistOpen":"0",
         "instructionMode":"T",
         "seatsCapacity":"95",
         "seatsFilled":"0",
         "academicGroup":null,
         "academicGroupDescr":null,
         "flags":[],
         "instructor":[           {"id":"Not Assigned",
               "name":"Not Assigned",
               "email":null}]},
         {"optional":false,
         "registrationClosed":false,
         "courseAttributes":null,
         "credits":"0",
         "creditsMin":0.0,
         "creditsMax":0.0,
         "openSeats":19,
         "meetings":[           {"days":"W",
               "daysRaw":"W",
               "startTime":800,
               "endTime":850,
               "location":"SL 123",
               "meetingType":"CLAS",
               "startDate":"2016-08-31T00:00:00Z",
               "endDate":"2016-10-12T00:00:00Z",
               "mapURL":null,
               "firstMonday":"2016-08-29T00:00:00Z",
               "lastMonday":"2016-10-10T00:00:00Z"}],
         "academicCareer":"Graduate, High School (Mass Academy), Undergraduate",
         "academicCareerDescr":"Graduate, High School (Mass Academy), Undergraduate",
         "academicCareerDescrShort":"Graduate, High School (Mass Academy), Undergraduate",
         "campus":"Main",
         "campusShort":null,
         "classAssociations":null,
         "campusCode":"1",
         "campusDescription":"Main",
         "component":"Lab",
         "corequisiteSections":[],
         "course":"1101",
         "customData":"",
         "department":"Computer Science",
         "description":"This course introduces principles of computation and programming with an emphasis on program design. Topics include the design, implementation and testing of programs that use a variety of data structures (such as structures, lists, and trees), functions, conditionals, recursion and higher-­‐order functions. Students will be expected to design simple data models, and implement and debug programs in a functional programming language. <br />     Recommended background: none. <br />Either CS 1101 or CS 1102 provides sufficient background for further courses in the CS department. Undergraduate credit may not be earned for both this course and CS 1102. <br />",
         "disabledReasons":[],
         "enrollmentStatus":null,
         "enrollmentRequirements":[],
         "exams":[],
         "fees":"",
         "freeFormTopics":null,
         "hasCorequisites":false,
         "hasSectionNotes":false,
         "hasPrerequisites":false,
         "id":"15460",
         "isHonors":false,
         "isWritingEnhanced":false,
         "location":null,
         "lrnComTitle":null,
         "notes":"",
         "partsOfTerm":"Fall 2016 - A Term",
         "prerequisites":"",
         "corequisites":"",
         "registrationNumber":"15460",
         "registrationType":null,
         "reserveCaps":[],
         "sectionAttributes":[],
         "sectionNumber":"AX01",
         "sectionStatus":"Active",
         "subject":"CS",
         "subjectId":null,
         "title":"INTRO TO PROGRAM DESIGN-LAB",
         "topicId":null,
         "topicTitle":null,
         "waitlist":"0",
         "waitlistOpen":"0",
         "instructionMode":"T",
         "seatsCapacity":"19",
         "seatsFilled":"0",
         "academicGroup":null,
         "academicGroupDescr":null,
         "flags":[],
         "instructor":[           {"id":"Not Assigned",
               "name":"Not Assigned",
               "email":null}]},
      {"optional": false,
           "registrationClosed": false,
           "courseAttributes": null,
           "credits": "0",
           "creditsMin": 0.0,
           "creditsMax": 0.0,
           "openSeats": 19,
           "meetings":[{"days": "W",
                   "daysRaw": "W",
                   "startTime": 900,
                   "endTime": 950,
                   "location": "SL 123",
                   "meetingType": "CLAS",
                   "startDate": "2016-08-31T00:00:00Z",
                   "endDate": "2016-10-12T00:00:00Z",
                   "mapURL": null,
                   "firstMonday": "2016-08-29T00:00:00Z",
                   "lastMonday": "2016-10-10T00:00:00Z"}],
           "academicCareer": "Graduate, High School (Mass Academy), Undergraduate",
           "academicCareerDescr": "Graduate, High School (Mass Academy), Undergraduate",
           "academicCareerDescrShort": "Graduate, High School (Mass Academy), Undergraduate",
           "campus": "Main",
           "campusShort": null,
           "classAssociations": null,
           "campusCode": "1",
           "campusDescription": "Main",
           "component": "Lab",
           "corequisiteSections": [],
           "course": "1101",
           "customData": "",
           "department": "Computer Science",
           "description": "This course introduces principles of computation and programming with an emphasis on program design. Topics include the design, implementation and testing of programs that use a variety of data structures (such as structures, lists, and trees), functions, conditionals, recursion and higher-­‐order functions. Students will be expected to design simple data models, and implement and debug programs in a functional programming language. <br />     Recommended background: none. <br />Either CS 1101 or CS 1102 provides sufficient background for further courses in the CS department. Undergraduate credit may not be earned for both this course and CS 1102. <br />",
           "disabledReasons": [],
           "enrollmentStatus": null,
           "enrollmentRequirements": [],
           "exams": [],
           "fees": "",
           "freeFormTopics": null,
           "hasCorequisites": false,
           "hasSectionNotes": false,
           "hasPrerequisites": false,
           "id": "10340",
           "isHonors": false,
           "isWritingEnhanced": false,
           "location": null,
           "lrnComTitle": null,
           "notes": "",
           "partsOfTerm": "Fall 2016 - A Term",
           "prerequisites": "",
           "corequisites": "",
           "registrationNumber": "10340",
           "registrationType": null,
           "reserveCaps": [],
           "sectionAttributes": [],
           "sectionNumber": "AX02",
           "sectionStatus": "Active",
           "subject": "CS",
           "subjectId": null,
           "title": "INTRO TO PROGRAM DESIGN-LAB",
           "topicId": null,
           "topicTitle": null,
           "waitlist": "0",
           "waitlistOpen": "0",
           "instructionMode": "T",
           "seatsCapacity": "19",
           "seatsFilled": "0",
           "academicGroup": null,
           "academicGroupDescr": null,
           "flags": [],
           "instructor":[{"id": "Not Assigned",
                   "name": "Not Assigned",
                   "email": null}]},
             {"optional":false,
         "registrationClosed":false,
         "courseAttributes":null,
         "credits":"3",
         "creditsMin":3.0,
         "creditsMax":3.0,
         "openSeats":95,
         "meetings":[            {"days":"MTThF",
               "daysRaw":"MTRF",
               "startTime":1000,
               "endTime":1050,
               "location":"FL PH-UPR",
               "meetingType":"CLAS",
               "startDate":"2016-08-25T00:00:00Z",
               "endDate":"2016-10-13T00:00:00Z",
               "mapURL":null,
               "firstMonday":"2016-08-22T00:00:00Z",
               "lastMonday":"2016-10-10T00:00:00Z"}],
         "academicCareer":"Graduate, High School (Mass Academy), Undergraduate",
         "academicCareerDescr":"Graduate, High School (Mass Academy), Undergraduate",
         "academicCareerDescrShort":"Graduate, High School (Mass Academy), Undergraduate",
         "campus":"Main",
         "campusShort":null,
         "classAssociations":null,
         "campusCode":"1",
         "campusDescription":"Main",
         "component":"Lecture",
         "corequisiteSections":[],
         "course":"1101",
         "customData":"",
         "department":"Computer Science",
         "description":"This course introduces principles of computation and programming with an emphasis on program design. Topics include the design, implementation and testing of programs that use a variety of data structures (such as structures, lists, and trees), functions, conditionals, recursion and higher-­‐order functions. Students will be expected to design simple data models, and implement and debug programs in a functional programming language. <br />     Recommended background: none. <br />Either CS 1101 or CS 1102 provides sufficient background for further courses in the CS department. Undergraduate credit may not be earned for both this course and CS 1102. <br />",
         "disabledReasons":[],
         "enrollmentStatus":null,
         "enrollmentRequirements":[],
         "exams":[],
         "fees":"",
         "freeFormTopics":null,
         "hasCorequisites":false,
         "hasSectionNotes":false,
         "hasPrerequisites":false,
         "id":"10344",
         "isHonors":false,
         "isWritingEnhanced":false,
         "location":null,
         "lrnComTitle":null,
         "notes":"",
         "partsOfTerm":"Fall 2016 - A Term",
         "prerequisites":"",
         "corequisites":"",
         "registrationNumber":"10344",
         "registrationType":null,
         "reserveCaps":[],
         "sectionAttributes":[],
         "sectionNumber":"A02",
         "sectionStatus":"Active",
         "subject":"CS",
         "subjectId":null,
         "title":"INTRO TO PROGRAM DESIGN",
         "topicId":null,
         "topicTitle":null,
         "waitlist":"0",
         "waitlistOpen":"0",
         "instructionMode":"T",
         "seatsCapacity":"95",
         "seatsFilled":"0",
         "academicGroup":null,
         "academicGroupDescr":null,
         "flags":[],
         "instructor":[            {"id":"Not Assigned",
               "name":"Not Assigned",
               "email":null}]}]}


a.add_regblocks(testrbs)
