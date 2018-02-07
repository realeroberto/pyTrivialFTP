# pyTrivialFTP

[![PyPI](https://img.shields.io/pypi/v/pyTrivialFTP.svg)](https://pypi.python.org/pypi/pyTrivialFTP)

The poor man's API for accessing data on a remote FTP repository.

### Usage

        $ python pyTrivialFTP/pyTrivialFTP.py --hostname localhost --username foo --password bar --wd ~
        Connected to localhost.
        Changed working directory to /tmp.
        Welcome to the pyTrivialFTP shell.  Type help or ? to list commands.

        (pyTrivialFTP) list
        Retrieved file list.

        ...

        (pyTrivialFTP) quit
