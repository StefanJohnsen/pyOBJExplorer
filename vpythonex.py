# vpythonex.py 
# 
# Python Script to Resolve Specific ZeroDivisionError in vpython.py
#
# Copyright (c) 2023 by FalconCoding
# Author: Stefan Johnsen
# Email: stefan.johnsen@outlook.com
#
# This software is released under the MIT License.
#
#-----------------------------------------------------------------------
#
# When we run the script from the command line and exit the 
# program, we encounter a ZeroDivisionError.
# The reason for this is an Exit function at the very beginning
# of vpython.py, which is also being registered with the atexit module.
#
#-----------------------------------------------------------------------
# 
# def Exit():
#    zero = 0.
#    print('exit')
#    a = 1.0/zero              -> ZeroDivisionError
#
# import atexit
# atexit.register(Exit)
#
# I think this is a default exit function that are meant to
# be override.
# 
# The trick to unregister this function can be found here
# https://python-forum.io/thread-40405-page-2.html
# and is implemented below
#
#-----------------------------------------------------------------------

import atexit
import vpython

def unregister_by_name(name):
    funs = []
 
    class Capture:
        def __eq__(self, other):
            funs.append(other)
            return False
 
    c = Capture()
    atexit.unregister(c)
    for func in funs:
        if func.__name__ == name:
            atexit.unregister(func)
 
unregister_by_name("Exit") # so, we unregister the function

from vpython import *