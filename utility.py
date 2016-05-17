""" utility.py

Author: Jacob Komissar

Date: 2016-04-10

File for utility functions for this project.
"""
import sys

def print_now(*args, **kwargs):
    """ Prints the arguments immediately by also flushing stdout. """
    print(*args, **kwargs)
    sys.stdout.flush()

def maybe_print_now(bool, *args, **kwargs):
    """ Prints the arguments immediately if bool is true. """
    if bool:
        print(*args, **kwargs)
        sys.stdout.flush()
