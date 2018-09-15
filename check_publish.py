#!/usr/bin/env python3

from subprocess import run, PIPE
from option import __version__
import re


search = run(['pip', 'search', 'option'], stdout=PIPE)
stdout = search.stdout.decode()
regex = re.compile(r'option\s+\((\d+\.\d+\.\d+)\)')
cur_version = regex.match(stdout).groups(1)[0].split('.')
new_version = __version__.split('.')
if new_version > cur_version:
    print("true")
