import os
from unittest import TestCase

from pyTrivialFTP import pyTrivialFTP

class Test(TestCase):
    def test(self):
        hostname = os.environ['PYTRIVIALFTP_HOSTNAME']
        username = os.environ['PYTRIVIALFTP_USERNAME']
        password = os.environ['PYTRIVIALFTP_PASSWORD']
        wd = os.environ['PYTRIVIALFTP_WD']

        conn = pyTrivialFTP(hostname, username, password, wd)
        conn.login()
        self.assertTrue(len(conn.list()) > 0)
        conn.close()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
