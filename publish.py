#!/usr/bin/env python3

from os import getenv
from subprocess import run
from sys import argv

from option import __version__

new_version = __version__.split('.')

if getenv('UPLOAD_COV') == 'true':
    _, pypi_user, pypi_pass = argv
    run(['poetry', 'publish', '--build', '-u', pypi_user, '-p', pypi_pass])
