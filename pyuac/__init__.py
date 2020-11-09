#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

"""
User Access Control for Microsoft Windows Vista and higher.  This is only for the Windows platform.

This will relaunch either the current script - with all the same command line parameters - or
else you can provide a different script/program to run.  If the current user doesn't normally
have admin rights, he'll be prompted for an admin password. Otherwise he just gets the UAC prompt.

Note that the prompt may simply shows a generic python.exe with "Publisher: Unknown" if the
python.exe is not signed. However, the standard python.org binaries are signed.

This is meant to be used something like this, where you decorate your command line script's
main function:

>>> from pyuac import main_requires_admin

>>> @main_requires_admin
... def main():
...    # your script main code here.
...    return

>>> if __name__ == "__main__":
...     main()

Alternatively, you can do something like this:

>>> import pyuac

>>> if __name__ == "__main__":
...    if not pyuac.isUserAdmin():
...        return pyuac.runAsAdmin()
...    # otherwise carry on doing whatever...
...    main()

See also this utility function which runs a function as admin and captures the stdout/stderr:

run_function_as_admin(my_main_function)

"""

from pyuac.admin import isUserAdmin, runAsAdmin
from pyuac.main_decorator import main_requires_admin

__all__ = [
    'isUserAdmin',
    'runAsAdmin',
    'main_requires_admin'
]
