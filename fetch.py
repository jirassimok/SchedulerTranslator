""" jsonFetcher.py

Author: Jacob Komissar
Author: Adam Goldsmith

Date: 2016-04-09/10

Program to get WPI Course Planner pages as strings.


Departments are stored as dictionaries in a list json.

"""
import requests
import re
import time
import json  # Probably should be using requests.Response.json() instead.
import getpass


# TODO: Change local from a boolean to a base filepath for the database.
class Fetch(object):
    regblocks = True  # A constant for use as the "rb" parameter.

    def __init__(self, *, readfile=None, local=False, port=8000):
        # self.page = None  # A page retrieved with set_page().
        self.term = ""  # The current term.
        self.termlist = []

        # If hosting_locally is truthy, the page-fetching functions will add
        # .json to the end of the appropriate URLs.
        self.hosting_locally = local
        self.session = None  # Placeholder

        if not local:
            self.url = "https://wpi.collegescheduler.com/api/terms"
            if readfile:
                with open(readfile) as f:
                    sid = f.readline()[:-1]
                    pin = f.readline()[:-1]
            else:
                sid = input("username:")
                pin = getpass.getpass("password:")
            self.start_session(sid, pin)
        else:  # if local
            self.url = "http://localhost:" + str(port) + "/terms"

    def start_session(self, sid, pin):
        """ Creates a valid scheduler session by logging in to bannerweb and
        navigating to the schduler.

        @param sid: username
        @param pin: password
        @return: True if successful. None if hosting locally..
        """
        if self.hosting_locally:  # Prevent large session initialization
            return None
        baseurl = "https://bannerweb.wpi.edu/pls/prod"
        urls = {
            'home': baseurl + "/twbkwbis.P_WWWLogin",
            'login': baseurl + "/twbkwbis.P_ValLogin",
            'logout': baseurl + "/twbkwbis.P_Logout",
            'registration': baseurl + "/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu",
            'sched_redirect': baseurl + "/csched.p_redirect"
        }
        s = requests.Session()
        success = False
        while not success:
            s.get(urls["home"])
            r = s.get(urls["login"], params={"sid": sid, "PIN": pin},
                      headers={'referer': urls["login"]})
            success = (r.status_code == 200)
            if not success:
                raise ConnectionError("Login failed.")
                # return None
                # print("Login failed, retrying")
                # time.sleep(5)
                # continue
        r = s.get(urls['sched_redirect'],
                  headers={'referer': urls["registration"]})

        r = s.get(re.findall(r'https://wpi\.collegescheduler\.com/'
                             r'index\.aspx\?ticket=[^\'"]*',
                             r.text)[0])

        self.session = s
        self.show_full_courses(r.text)

        return True  # So the function always returns.

    def show_full_courses(self, entry_page):
        """ Sets the scheduler to show courses that are full.
        @param entry_page The page recieved upon entry to the scheduler.
        """
        # Everything from here to the actual request info could be replaced by:
        # field = re.search(r'<input name="__RequestVerificationToken"[^>]*/>',
        #                   entry_page)
        # token = re.search(r'(?<=value=")[^"]+(?=")', field)

        regex = r'<input name="__RequestVerificationToken"[^>]*/>'
        token_html_inputs = re.findall(regex, entry_page)

        regex = r'(?<=value=")[^"]+(?=")'
        tokens = []
        for field in token_html_inputs:
            matches = re.findall(regex, field)
            for match in matches:
                tokens.append(match)

        # Ensure that only one token is good to use.
        # Only the final else should ever actually run.
        if len(tokens)==0:
            raise Exception("Verification token not found"
                            "- could not get all courses")
            # TODO: Implement an option to ignore this error and proceed without full courses.
        elif len(tokens) > 1:
            print("Multiple verification tokens found, please choose one:")
            for i, token in enumerate(tokens):
                print(i, ": ", token, sep="")
            choice = input("Choose one of the numbers on the left: ")
            while choice not in [str(i) for i in range(len(tokens))]:
                choice = input("Choose one of the numbers on the left: ")
            token = tokens[int(choice)]
        else:  # one token
            token = tokens[0]

        headers = {
            "X-XSRF-Token": token,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json"
            }
        url = "https://wpi.collegescheduler.com/api/coursestatuses/OpenAndFull/selected"
        body = ('{id: "OpenAndFull", title: "Open & Full", '
                'selected: true, code: "OpenAndFull"}')

        self.session.put(url, body, headers=headers)


    def set_terms(self, *termstrings):
        """ Sets the current term, and adds additional terms to termlist.

        If multiple termstrings are provided, self.term is not guaranteed to be
        set to the first.
        @param termstrings: Strings representing the terms.
        """
        termset = {term.strip("/") for term in termstrings}
        self.termlist = list(termset)
        self.term = self.termlist[0]

    def get(self, term=None, dept=None, num=None,
            *, rb=True, clean=False, delay=0):
        """ Gets a page based on the arguments.

        Depending on how many arguments are given, different pages will be
        retrieved.
        In standard use, self.term should be passed as term.

        @param term: The term to get. As last, this will fetch the term list.
        @param dept: The department to get. As last, will fetch course list.
        @param num: The course's number. As last, will fetch course information.
        @param rb: If true, the course's registration blocks will be fetched.
        @param clean: If false, the data will not be cleaned for schedb parsing.
        @param delay: How long to wait before fetching the page.
        @return: The retrieved page.
        """
        time.sleep(delay)
        target = self.url
        if term:
            target += "/" + term + "/subjects"
            if dept:
                target += "/" + dept + "/courses"
                if num:
                    target += "/" + str(num)
                    if rb:
                        target += "/regblocks"
        target += ".json" if self.hosting_locally else ""
        # print(target)
        if self.hosting_locally:
            response = requests.get(target)
        else:
            response = self.session.get(target)
        response.raise_for_status()  # Error if request fails, None otherwise
        page = response.text
        if clean:
            page = Fetch.clean_page(page)
        # print('\n', target, '\n', page)
        return page

    def get_json(self, term=None, dept=None, num=None, rb=True):
        return json.loads(self.get(term, dept, num, rb=rb, clean=False))

    # def set_page(self, term=None, dept=None, num=None, rb=False,
    #              *, clean=False):
    #     self.page = self.get(term, dept, num, rb, clean=clean)

    # def set_json(self):
    #     self.page = self.page.json()
    #     # self.page = json.loads(self.page)

    @staticmethod
    def clean_page(page):
        return (page.replace('<br />', ' ').replace('&', '&amp;')
                .encode("ascii", errors="ignore").decode("ascii"))
        # .replace("<", "&lt;")
        # .replace('&', '&amp;')
        # .replace(u"\u2019", "'")