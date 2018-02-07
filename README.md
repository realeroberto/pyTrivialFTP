# pyTrivialFTP

[![PyPI](https://img.shields.io/pypi/v/pyTrivialFTP.svg)](https://pypi.python.org/pypi/pyTrivialFTP)

The poor man's API for accessing data on a remote FTP repository.

### Usage

As a standalone script:

        $ python pyTrivialFTP/pyTrivialFTP.py --hostname localhost --username foo --password bar --wd ~
        Connected to localhost.
        Changed working directory to /tmp.
        Welcome to the pyTrivialFTP shell.  Type help or ? to list commands.

        (pyTrivialFTP) list
        Retrieved file list.

        ...

        (pyTrivialFTP) quit

As a module:

        from pyTrivialFTP import pyTrivialFTP

        conn = pyTrivialFTP('localhost', 'foo', 'bar', '~')
        conn.login()
        conn.list()
        conn.close()
