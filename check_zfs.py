#!/usr/bin/python3

"""
A simple python3 script that parses zpool status to check the status of a pool.
supports parse of: state, status, and error fields

Copyright (c) 2020 Alex Yeo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import subprocess
from shlex import quote #for security
import sys

def return_ok(msg):
    print("OK: {}".format(msg))
    exit(0)

def return_warning(msg):
    print("WARNING: {}".format(msg))
    exit(1)

def return_critical(msg):
    print("CRITICAL: {}".format(msg))
    exit(2)

def return_unknown(msg):
    print("UNKNOWN: {}".format(msg))
    exit(3)

POOL_NAME=None

if __name__ == "__main__":
    if POOL_NAME == None:
        return_unknown("No pool specified.")
    if len(sys.argv) < 2:
        return_unknown("No pool name arg given.")
    POOL_NAME = sys.argv[1]

    zfs_status = subprocess.Popen(['zpool', 'status', quote(POOL_NAME)],  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = zfs_status.communicate()
    if stderr == None:
        cmd_output = quote(stdout.decode("utf-8"))
        if "no such pool" in cmd_output:
            return_critical("Pool not found!")

        pool_state = None
        pool_errors = None
        pool_status = None
        for line in cmd_output.split('\n'):
            if "state: " in line:
                pool_state = line.split(': ')[1]
            if "errors: " in line:
                pool_errors = line.split(': ')[1]
            if "status: " in line:
                pool_status = line.split(': ')[1]

        if pool_status == None:
            pool_status = ""
        #determine state
        if pool_state == None:
            return_warning("Cannot get pool state.")
        if "ONLINE" in pool_state:
            return_ok("Status {}.".format(pool_state))
        else:
            return_critical("State {}. Status: ".format(pool_state,pool_status))
        #parse status first, then errors
        if pool_errors == None:
             return_warning("Cannot parse errors.")
        if "No known data errors" not in pool_errors:
             return_critical("Errors present: {}".format(quote(pool_errors)))

    else:
        return_unknown("Command failed (stderr): ".format(quote(stderr.decode("utf-8"))))
