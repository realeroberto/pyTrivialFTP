# pyTrivialFTP
# The poor man's API for accessing data on a remote FTP repository

# The MIT License (MIT)
#
# Copyright (c) 2014-5 Roberto Reale <roberto.reale82@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__author__ = "Roberto Reale"
__version__ = "0.1.0"


from ConfigParser import ConfigParser
from ftplib import FTP, error_perm
import re
import logging
import logging.config


class pyTrivialFTPConfig(ConfigParser):

    @property
    def logger(self):
        return self.get(self._section, 'logger')

    @property
    def hostname(self):
        return self.get(self._section, 'hostname')

    @property
    def username(self):
        return self.get(self._section, 'username')

    @property
    def password(self):
        return self.get(self._section, 'password')

    @property
    def wd(self):
        return self.get(self._section, 'wd')

    @property
    def filter(self):
        return self.get(self._section, 'filter')

    @property
    def filter_match(self):
        pattern = re.compile(self.filter)
        def match(s):
            return pattern.match(s)
        return match

    def __init__(self, config_file, trivial_ftp_name='trivial_ftp'):
        ConfigParser.__init__(self)
        self.read(config_file)
        self._section = trivial_ftp_name

    def __del__(self):
        pass


class pyTrivialFTP(pyTrivialFTPConfig, FTP):

    def login(self):
        if not self.connected:
            FTP.login(self, self.username, self.password)
            self.connected = True
            self.log(20, "Connected to %s." % self.hostname)
            self.cwd(self.wd)
            self.log(20, "Changed working directory to %s." % self.wd)
        else:
            self.log(10, "Already connected.")

    def close(self):
        # logout from the remote site
        if self.connected:
            FTP.close(self)
            self.connected = False
            self.log(20, "Disconnected from %s." % self.hostname)
        else:
            self.log(10, "Already disconnected from %s." % self.hostname)

    def list(self):
        try:
            files = self.nlst()
            self.log(20, "Retrieved file list.")
        except error_perm, resp:
            if str(resp) == "550 No files found":
                self.log(10, "File list is empty.")
                return None
            else:
                raise
        return filter(self.filter_match, files)

    def copy(self, filename, callback, binary=False):
        if binary:
            self.retrbinary("RETR " + filename, callback)
        else:
            self.retrlines("RETR " + filename, callback)
        self.log(20, "Retrieved file %s." % filename)

    def __init__(self, config_file, trivial_ftp_name='trivial_ftp', autologin=False):
        # set defaults
        self.connected = False
        # parse config file
        pyTrivialFTPConfig.__init__(self, config_file, trivial_ftp_name)
        # initialize and start logging
        logging.config.fileConfig(config_file)
        self.logger_logger = logging.getLogger(self.logger)
        self.log = self.logger_logger.log
        # initialize FTP connector
        FTP.__init__(self, self.hostname)
        # login to the remote site
        if autologin:
            self.login()

    def __del__(self):
        pass
