#!/usr/bin/env python3

import re
from os import getenv
from subprocess import PIPE, run
from sys import argv

from option import __version__

search = run(['pip', 'search', 'option'], stdout=PIPE)
stdout = search.stdout.decode()
print(stdout)

regex = re.compile(r'option\s+\((\d+\.\d+\.\d+)\)')
cur_version = regex.match(stdout).groups(1)[0].split('.')
new_version = __version__.split('.')
print(f'Current version: {cur_version}, New version: {new_version}')

if new_version > cur_version and getenv('UPLOAD_COV') == 'true':
    _, pypi_user, pypi_pass = argv
    run(['poetry', 'publish', '--build', '-u', pypi_user, '-p', pypi_pass])
