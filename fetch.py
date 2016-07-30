""" jsonFetcher.py

Author: Adam Goldsmith
Author: Jacob Komissar

Date: 2016-04-09/10

Program to get WPI Course Planner pages as strings.


Departments are stored as dictionaries in a list json.

"""
import re
import time
import json  # Probably should be using requests.Response.json() instead.
import getpass
import requests


# TODO: Change local from a boolean to a base filepath for the database.
class Fetch(object):
    regblocks = True  # A constant for use as the "rb" parameter.

    def __init__(self, *, readfile=None, local=None):
        # self.page = None  # A page retrieved with set_page().

        # If local_db is truthy, the page-fetching functions will add
        # .json to the end of the appropriate URLs.
        self.local_db = local
        self.session = None  # Placeholder

        if local is None:
            self.url = "https://wpi.collegescheduler.com/api"
            if readfile:
                with open(readfile) as f:
                    sid = f.readline().strip()
                    pin = f.readline().strip()
            else:
                sid = input("username:")
                pin = getpass.getpass("password:")
            self.start_session(sid, pin)

    def start_session(self, sid, pin):
        """ Creates a valid scheduler session by logging in to bannerweb and
        navigating to the schduler.

        @param sid: username
        @param pin: password
        @return: True if successful. None if hosting locally..
        """
        baseurl = "https://bannerweb.wpi.edu/pls/prod"
        urls = {
            'home': baseurl + "/twbkwbis.P_WWWLogin",
            'login': baseurl + "/twbkwbis.P_ValLogin",
            'logout': baseurl + "/twbkwbis.P_Logout",
            'registration': baseurl + "/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu",
            'sched_redirect': baseurl + "/csched.p_redirect"
        }
        s = requests.Session()
        # Log in to bannerweb
        s.get(urls["home"])
        r = s.get(urls["login"], params={"sid": sid, "PIN": pin},
                  headers={'referer': urls["login"]})
        if not r.status_code == 200:
            raise ConnectionError("Login failed.")
        # Get the redirect page
        r = s.get(urls['sched_redirect'],
                  headers={'referer': urls["registration"]})

        # Find the link with the ticket and log in to collegescheduler with it
        r = s.get(re.findall(r'https://wpi\.collegescheduler\.com/'
                             r'index\.aspx\?ticket=[^\'"]*',
                             r.text)[0])

        self.session = s
        self.show_full_courses(r.text)


    def show_full_courses(self, entry_page):
        """ Sets the scheduler to show courses that are full.
        @param entry_page The page recieved upon entry to the scheduler.
        """
        field = re.findall(r'<input name="__RequestVerificationToken".*/>',
                           entry_page)[0]
        token = re.findall(r'(?<=value=")[^"]+(?=")', field)[0]

        headers = {
            "X-XSRF-Token": token,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json"
            }
        url = self.url + "coursestatuses/OpenAndFull/selected"
        body = ('{id: "OpenAndFull", title: "Open & Full", '
                'selected: true, code: "OpenAndFull"}')

        self.session.put(url, body, headers=headers)


    def create_path(self, term=None, dept=None, num=None, rb=True):
        """Assembles a path for a file from the parts

        @param term: The term to get. As last, this will fetch the term list.
        @param dept: The department to get. As last, will fetch course list.
        @param num: The course's number. As last, will fetch course information.
        @param rb: If true, the course's registration blocks will be fetched.
        @return the path
        """
        target = "/terms"
        if term:
            target += "/" + term + "/subjects"
            if dept:
                target += "/" + dept + "/courses"
                if num:
                    target += "/" + str(num)
                    if rb:
                        target += "/regblocks"
        target += ".json" if self.local_db is not None else ""
        return target

    def get(self, path, delay=0):
        """ Gets a page based on the arguments.

        Depending on how many arguments are given, different pages will be
        retrieved.

        @param path: The path to the page to get.
        @param clean: If false, the data will not be cleaned for schedb parsing.
        @param delay: How long to wait before fetching the page.
        @return: The retrieved page.
        """
        time.sleep(delay)
        if self.local_db is not None:
            with open(self.local_db + path.replace("%20", " ")) as file:
                page = file.read()
        else:
            target = self.url + path
            response = self.session.get(target)
            response.raise_for_status()  # Error if request fails, None otherwise
            page = response.text
        return page

    def get_json(self, path):
        return json.loads(self.get(path))
