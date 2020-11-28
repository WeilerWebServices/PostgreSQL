import re
import requests
from io import StringIO
import dateutil.parser
from datetime import timedelta

from html.parser import HTMLParser

from lib.log import log


class GenericHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.lasttag = None
        self.title = ""
        self.pagedata = StringIO()
        self.links = []
        self.inbody = False

    def handle_starttag(self, tag, attrs):
        self.lasttag = tag
        if tag == "body":
            self.inbody = True
        if tag == "a":
            for a, v in attrs:
                if a == "href":
                    self.links.append(v)

    def handle_endtag(self, tag):
        if tag == "body":
            self.inbody = False

    DATA_IGNORE_TAGS = ("script",)

    def handle_data(self, data):
        d = data.strip()
        if len(d) < 2:
            return

        if self.lasttag == "title":
            self.title += d
            return

        # Never store text found in the HEAD
        if not self.inbody:
            return

        # Ignore specific tags, like SCRIPT
        if self.lasttag in self.DATA_IGNORE_TAGS:
            return

        self.pagedata.write(d)
        self.pagedata.write("\n")

    def gettext(self):
        self.pagedata.seek(0)
        return self.pagedata.read()


class RobotsParser(object):
    def __init__(self, url):
        try:
            r = requests.get(url)
            self.disallows = []
            activeagent = False
            for l in r.text.splitlines():
                if l.lower().startswith("user-agent: ") and len(l) > 12:
                    if l[12] == "*" or l[12:20] == "pgsearch":
                        activeagent = True
                    else:
                        activeagent = False
                if activeagent and l.lower().startswith("disallow: "):
                    self.disallows.append(l[10:])
        except Exception:
            self.disallows = []

    def block_url(self, url):
        # Assumes url comes in as relative
        for d in self.disallows:
            if url.startswith(d):
                return True
        return False
