"""General utilities for writing scrapers for CiteULike in Python"""

from htmlentitydefs import name2codepoint
from urlparse import urlparse
import HTMLParser
import cgi
import os
import re
import signal
import sys


def decode_entities(html):
    return unicode(HTMLParser.HTMLParser().unescape(html))


def x_decode_entities(html):
    html = re.sub('&#(\d+);', lambda m: unichr(int(m.group(1))), html)
    code_point = lambda m: str(name2codepoint[m.group(1)])
    html = re.sub('&(%s);' % '|'.join(name2codepoint), code_point, html)
    return html


def handleSig(signum, frame):
    sys.exit(0)


def install_io_trap():
    signal.signal(signal.SIGPIPE, handleSig)
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


def remove_querystring(url):
    return re.sub(r'\?.*', '', url)


def bail(msg):
    print "status\terr\t", msg
    sys.exit(1)


def urlparams(url):
    ret = {}
    for (key, val) in cgi.parse_qsl(urlparse(url)[4]):
        ret[key.lower()] = val
    return ret
