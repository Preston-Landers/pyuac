#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

"""
Test the main_requires_admin decorator

Note the test is not fully automatic unless the UAC prompt is disabled at the Windows
system level. Otherwise, someone has to click on the UAC prompts.
"""

import os
import sys

from pyuac import isUserAdmin, main_requires_admin

here = os.path.abspath(__file__)


def sample_function_body(arg1, kwarg2='Default'):
    print("Hello, world.")
    is_admin = isUserAdmin()
    print("isUserAdmin: %s" % (is_admin,))
    print("arg1: %s" % (arg1,))
    print("kwarg2: %s" % (kwarg2,))
    return


example1_args = ('foobar',)
example1_kwargs = {'kwarg2': 'biz'}


@main_requires_admin(return_output=True)
def example1_main():
    sample_function_body(*example1_args, **example1_kwargs)
    # input("Press Enter >")
    return


def test_run_function_with_output():
    expected_output = """Hello, world.
isUserAdmin: True
arg1: foobar
kwarg2: biz
"""
    cmdLine = [sys.executable, here, 'example1']
    decorated_sample = main_requires_admin(
        sample_function_body, return_output=True, cmdLine=cmdLine)
    rv = decorated_sample(*example1_args, **example1_kwargs)
    assert rv, "Already ran as admin?"
    actual_stdout, actual_stderr, *_ = rv
    assert actual_stdout == expected_output
    assert actual_stderr == ""
    return


TMP_FILE_NAME = 'test_decorator.py.tmp'
example2_args = ('happy! day',)
example2_kwargs = {'kwarg2': 'Here are \'quotes\' "embedded"'}


def sample_function_write_file(arg1, kwarg2='Default'):
    with open(TMP_FILE_NAME, "w") as fh:
        data = ["Hello, world."]
        is_admin = isUserAdmin()
        data.append("isUserAdmin: %s" % (is_admin,))
        data.append("arg1: %s" % (arg1,))
        data.append("kwarg2: %s" % (kwarg2,))
        fh.write("\n".join(data) + "\n")


@main_requires_admin
def example2_main():
    sample_function_write_file(*example2_args, **example2_kwargs)
    # input("Press Enter >")
    return


def test_run_function_no_output():
    expected_output = """Hello, world.
isUserAdmin: True
arg1: happy! day
kwarg2: Here are 'quotes' "embedded"
"""
    cmdLine = [sys.executable, here, 'example2 has spaces and "quote\'s"']
    decorated_sample = main_requires_admin(
        sample_function_body, return_output=False, cmdLine=cmdLine)
    rv = decorated_sample(*example2_args, **example2_kwargs)
    assert rv is None
    with open(TMP_FILE_NAME, 'r') as fh:
        actual_output = fh.read()
    if os.path.exists(TMP_FILE_NAME):
        os.unlink(TMP_FILE_NAME)
    assert actual_output == expected_output
    return


if __name__ == '__main__':
    if sys.argv[1] == "example1":
        example1_main()
    elif sys.argv[1] == 'example2 has spaces and "quote\'s"':
        example2_main()
