#!/usr/bin/env python3
#
# This hook script is run by gitdeployer when the code is
# deployed to a server. figure out which templates have been
# modified and queue automatic purges for them.
# Gitdeployer will pass a list of all modified files on
# stdin.

import sys
import os
import hashlib
from configparser import ConfigParser
import psycopg2

# Templates that we don't want to ban automatically
BANNED_TEMPLATES = (
    'base/base.html',
)

if __name__ == "__main__":
    config = ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'purgehook.ini'))
    conn = psycopg2.connect(config.get('db', 'dsn'))
    curs = conn.cursor()

    for l in sys.stdin:
        if l.startswith('templates/'):
            tmpl = l[len('templates/'):].strip()
            if tmpl not in BANNED_TEMPLATES:
                curs.execute("SELECT varnish_purge_xkey(%(key)s)", {
                    'key': 'pgwt_{0}'.format(hashlib.md5(tmpl.encode('ascii')).hexdigest()),
                })
        elif l.startswith('media/'):
            # For media we can't xkey, but the URL is exact so we can
            # use a classic single-url purge.
            curs.execute("SELECT varnish_purge('^/' || %(u)s || '$')", {
                'u': l.strip(),
            })
    conn.commit()
    conn.close()
