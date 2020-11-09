#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

"""
See main_requires_admin
"""

from __future__ import absolute_import

import os
import sys
from logging import getLogger

from decorator import decorator
from tee import StderrTee, StdoutTee

from pyuac import isUserAdmin, runAsAdmin

log = getLogger(__name__)


@decorator
def main_requires_admin(
    run_function,
    cmdLine=None,
    return_output=False,
    stdout_handle=None, stderr_handle=None,
    scan_for_error=('error', 'exception'),
    *args, **kwargs
):
    """
    A decorator for a Python script 'main' function (i.e., when the file is invoked from the
    command line as a script) that ensures the 'main' function is executed as an Admin.
    Implements a common usage pattern of this module, which allows for capturing the stdout and
    stderr output from the sub-process and a very basic scan for errors.

    There is strong assumption here that when the current Python script is re-executed in the
    admin context with the same command line args, it code logic will lead to this same decorated
    main function being executed again.

    You can NOT send data from the parent (non-admin) process to the child (Admin)
    process. Depending on how the parent process was invoked, the child process
    might spawn a Python console window that can be interacted with directly.

    Warning: this does not allow capture of the process return code for error detection.
    However, the scan_for_error option will look for the case-ins string "error" on the last line
    (only) of output, or 'exception', and raise a RuntimeError with the string if found.

    :param run_function: the function to run
    :param args: arguments tuple to pass to run_function when called (optional)
    :param kwargs: keyword arguments dict to pass to run_function when called (optional)
    :param cmdLine: override the command line arguments for the new Admin process.
        Defaults to the current command line (sys.argv)!
    :param return_output: return the output to the caller of this function instead
        of writing it to stdout_handle. Note: due to the nature of how this works with UAC,
        this does NOT return the actual "return value" of run_function - only its
        stdout and stderr output (as a 2-tuple of (stderr, stdout). If you set this, the callers
        of your decorated function should be prepared for this output.
    :param stdout_handle: file handle to write the process stdout output, defaults to sys.stdout
    :param stderr_handle: file handle to write the process stderr output, defaults to sys.stderr
    :param scan_for_error: scan the LAST line only of stdout and stderr for the listed strings.
        Case is ignored. Set to None or False to disable this. If one of the listed strings
        is found, a RuntimeError is raised in the parent process.
    :return: None unless return_output is set.
        If return_output is True, the output of the decorated function is a 2-tuple
        of (stdout, stderr) strings.
    """
    if os.name != 'nt':
        log.debug("Invoked main_requires_admin on a non-Windows platform; doing nothing!")
        return run_function(*args, **kwargs)

    # Should we add another function parameter to run the in the "not-admin" case?

    # Generate secure temp path? - path has to be known in spawned process...
    stdout_temp_fn = 'pyuac.stdout.tmp.txt'
    stderr_temp_fn = 'pyuac.stderr.tmp.txt'

    if stdout_handle is None:
        stdout_handle = sys.stdout
    if stderr_handle is None:
        stderr_handle = sys.stderr

    if isUserAdmin():
        with StdoutTee(stdout_temp_fn, mode="a", buff=1), \
             StderrTee(stderr_temp_fn, mode="a", buff=1):
            try:
                log.debug("Starting run_function as admin")
                rv = run_function(*args, **kwargs)
                log.debug("Finished run_function as admin. return val: %r", rv)
                return rv
            except Exception:
                log.error("Error running main function as admin", exc_info=True)
                raise
    else:
        log.debug("I'm not admin, starting runAsAdmin")
        runAsAdmin(cmdLine=cmdLine, wait=True)
        log.debug("I'm not admin, runAsAdmin has finished. Collecting result.")

        rv = []
        for filename, handle in (
            (stdout_temp_fn, stdout_handle),
            (stderr_temp_fn, stderr_handle),
        ):
            if os.path.exists(filename):
                with open(filename, "r") as log_fh:
                    console_output = log_fh.read()
                os.remove(filename)
                if os.path.exists(filename):
                    log.warning("Couldn't delete temporary log file %s", filename)

                if scan_for_error:
                    lines = str.splitlines(console_output.strip())
                    if lines:
                        last_line = lines[-1].strip()
                        for error_str in scan_for_error:
                            if last_line.lower().find(error_str) != -1:
                                log.info(
                                    "Identified an error line in Admin process log at %s - "
                                    "emitting RuntimeError in parent process.\n%s",
                                    filename, last_line)
                                raise RuntimeError(last_line)

                if return_output:
                    # return console_output
                    rv.append(console_output)

                handle.write(console_output)
                handle.flush()

        if return_output and rv:
            return rv
