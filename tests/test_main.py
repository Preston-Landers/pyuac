#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

"""
Test the basic functions isUserAdmin and runAsAdmin.

Note the test is not fully automatic unless the UAC prompt is disabled at the Windows
system level. Otherwise, someone has to click on the UAC prompts.
"""

from __future__ import print_function

import os
import sys

from pyuac import isUserAdmin, runAsAdmin


def test_1_not_admin():
    """
    The test should not be launched as admin.
    :return:
    """
    is_admin = isUserAdmin()
    assert not is_admin, "You should launch this test as a regular non-admin user."


def test_can_run_as_admin():
    """
    A simple test function; check if we're admin, and if not relaunch
    the script as admin.
    """
    if not isUserAdmin():
        print("You're not an admin.", os.getpid(), "params: ", sys.argv)
        # rc = runAsAdmin(["c:\\Windows\\notepad.exe"])
        rc = runAsAdmin()
    else:
        print("You are an admin!", os.getpid(), "params: ", sys.argv)
        rc = 0
    # input('Press Enter to exit. >')
    return rc
