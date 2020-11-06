#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

"""
See run_function_as_admin_with_output

TODO: this is unfinished and untested
"""

import sys
import os
import traceback

from tee import StderrTee, StdoutTee

from pyuac import isUserAdmin, runAsAdmin


def run_function_as_admin_with_output(
    run_function, run_args=None, run_kwargs=None,
    return_output=False, stdout_handle=None, stderr_handle=None,
    scan_for_error=True,
    stdout_temp_fn=None, stderr_temp_fn=None,
):
    """
    Implements a common usage pattern of this module, which allows for capturing the stdout and
    stderr output from the sub-process.

    You can NOT otherwise interact with the sub-process (supply input to it) at least through
    standard input.

    Warning: this does not allow capture of the process return code for error detection.
    However, the scan_for_error option will look for the case-ins string "error" on the last line
    (only) of output, and raise a RuntimeError with the string if found.

    @param run_function: the function to run
    @param run_args: arguments tuple to pass to run_function when called (optional)
    @param run_kwargs: keyword arguments dict to pass to run_function when called (optional)
    @param return_output: return the output to the caller of this function instead
        of writing it to stdout_handle. Note: due to the nature of how this works with UAC,
        this does NOT return the actual "return value" of run_function - only its
        stdout and stderr output (as a 2-tuple of (stderr, stdout)
    @param stdout_handle: file handle to write the process stdout output, defaults to sys.stdout
    @param stderr_handle: file handle to write the process stderr output, defaults to sys.stderr
    @param scan_for_error: look at the last line only for the string 'error' and
        turn that into a RuntimeError if found.
    @param stdout_temp_fn: the name of the temporary log file to use (will be deleted)
        for standard output stream of the sub-process. If not given, a default is generated
    @param stderr_temp_fn: the name of the temporary log file to use (will be deleted)
        for standard error stream of the sub-process. If not given, a default is generated
    @return: None unless return_output is set
    """

    # Should we add another function parameter to run the in the "not-admin" case?

    # TODO: generate secure temp path?
    if stdout_temp_fn is None:
        stdout_temp_fn = 'pyuac.stdout.tmp.txt'
    if stderr_temp_fn is None:
        stderr_temp_fn = 'pyuac.stderr.tmp.txt'

    if stdout_handle is None:
        stdout_handle = sys.stdout
    if stderr_handle is None:
        stderr_handle = sys.stderr

    if run_kwargs is None:
        run_kwargs = {}
    if run_args is None:
        run_args = ()

    if isUserAdmin():
        with StdoutTee(stdout_temp_fn, mode="w"), StderrTee(stderr_temp_fn, mode="w"):
            # noinspection PyBroadException
            try:
                run_function(*run_args, **run_kwargs)
            except:
                # TODO: re-raise here?
                traceback.print_exc(file=stderr_handle)
    else:
        runAsAdmin(wait=True)
        # TODO: add stderr handling
        if os.path.exists(stdout_temp_fn):
            with open(stdout_temp_fn, "r") as log_fh:
                console_output = log_fh.read()
            os.remove(stdout_temp_fn)
            if os.path.exists(stdout_temp_fn):
                print("Warning, can't delete " + stdout_temp_fn)

            if scan_for_error:
                last_line = str.splitlines(console_output.strip())[-1].strip()
                if last_line.lower().find("error") != -1:
                    raise RuntimeError(last_line)

            if return_output:
                return console_output

            stdout_handle.write(console_output)
            stdout_handle.flush()
