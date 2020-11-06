#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

"""

"""

from pyuac import isUserAdmin
from pyuac.run_function import run_function_as_admin


def sample_function_body(arg1, kwarg2='Default'):
    print("Hello, world.")
    is_admin = isUserAdmin()
    print("isUserAdmin: %s" % (is_admin,))
    print("arg1: %s" % (arg1,))
    print("kwarg2: %s" % (kwarg2,))
    return


def test_run_function():
    expected_output = """Hello, world.
isUserAdmin: True
arg1: foobar
kwarg2: biz
"""
    actual_stdout, actual_stderr = run_function_as_admin(
        sample_function_body,
        ('foobar',),
        {'kwarg2': 'biz'},
        return_output=True
    )
    assert actual_stdout == expected_output
    assert actual_stderr == ""
    return
