#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

"""User Access Control for Microsoft Windows Vista and higher.  This is only for the Windows
platform.

This will relaunch either the current script - with all the same command line parameters - or
else you can provide a different script/program to run.  If the current user doesn't normally
have admin rights, he'll be prompted for an admin password. Otherwise he just gets the UAC prompt.

Note that the prompt may simply shows a generic python.exe with "Publisher: Unknown" if the
python.exe is not signed. However, the standard python.org binaries are signed.

This is meant to be used something like this::

    if not pyuac.isUserAdmin():
        return pyuac.runAsAdmin()

    # otherwise carry on doing whatever...

See also this utility function which runs a function as admin and captures the stdout/stderr:

run_function_as_admin_with_output(my_main_function)

"""

import os
import sys
from logging import getLogger

log = getLogger('pyuac')


def isUserAdmin():
    """Check if the current OS user is an Administrator or root.

    :return: True if the current user is an 'Administrator', otherwise False.
    """
    if os.name == 'nt':
        import win32security

        try:
            adminSid = win32security.CreateWellKnownSid(
                win32security.WinBuiltinAdministratorsSid, None)
            rv = win32security.CheckTokenMembership(None, adminSid)
            log.info("isUserAdmin - CheckTokenMembership returned: %r", rv)
            return rv
        except Exception as e:
            log.warning("Admin check failed, assuming not an admin.", exc_info=e)
            return False
    else:
        # Check for root on Posix
        return os.getuid() == 0


def runAsAdmin(cmdLine=None, wait=True):
    """
    Attempt to relaunch the current script as an admin using the same command line parameters.

    WARNING: this function only works on Windows. Future support for Posix might be possible.
    Calling this from other than Windows will raise a RuntimeError.

    :param cmdLine: set to override the command line of the program being launched as admin.
    Otherwise it defaults to the current process command line! It must be a list in
    [command, arg1, arg2...] format.

    :param wait: Set to False to avoid waiting for the sub-process to finish. You will not
    be able to fetch the exit code of the process if wait is False.

    :returns: the sub-process return code, unless wait is False, in which case it returns None.
    """

    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.")

    import win32con
    import win32event
    import win32process
    # noinspection PyUnresolvedReferences
    from win32com.shell.shell import ShellExecuteEx
    # noinspection PyUnresolvedReferences
    from win32com.shell import shellcon

    if cmdLine is None:
        cmdLine = [sys.executable] + sys.argv
        log.debug("Defaulting to runAsAdmin command line: %r", cmdLine)
    elif type(cmdLine) not in (tuple, list):
        raise ValueError("cmdLine is not a sequence.")
    cmd = '"%s"' % (cmdLine[0],)
    # XXX TODO: isn't there a function or something we can call to massage command line params?
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    showCmd = win32con.SW_SHOWNORMAL
    lpVerb = 'runas'  # causes UAC elevation prompt.

    log.info("Running command %r - %r", cmd, params)

    procInfo = ShellExecuteEx(
        nShow=showCmd,
        fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
        lpVerb=lpVerb,
        lpFile=cmd,
        lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']
        _ = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        log.info("Process handle %s returned code %s", procHandle, rc)
    else:
        rc = None

    return rc
