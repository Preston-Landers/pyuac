# PyUAC - Python User Access Control

This package provides a way to invoke User Access Control (UAC) in Windows from Python.

This allows a Python process to elevate itself to Administrator level rights using the UAC prompt.

## Quick Usage

There are two main functions provided:

    isUserAdmin()
This returns a boolean to indicate whether the current user has elevated Administrator status.

    runAsAdmin()
Re-launch the current process (or the given command line) as an Administrator. 
This will trigger the UAC (User Access Control) prompt if necessary.

### Example Usage

```
import pyuac

def main():
    print("This part needs to be run as an admin.")

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        return pyuac.runAsAdmin()
    main()
```

## Requirements

* This package only supports Windows at the moment. The isUserAdmin function will work under
  Linux / Posix, but the runAsAdmin command is currently Windows only.
  
* This requires Python 2.7, or Python 3.3 or higher.

* This requires the PyWin32 package to be installed.

https://pypi.org/project/pywin32/
https://github.com/mhammond/pywin32

## PyWin32 problems

The PyWin32 package is required by this library (pyuac).

If you get ImportErrors when you run this on the win32* modules (win32event or win32com)
usually that means PyWin32 is either not installed at all, or else the installation is incomplete;
see below.

PyWin32 can be installed via pip, but sometimes there are problems completing the installation
scripts which install the COM object support required by pyuac. 

Typically, this can be fixed doing the following:
 
* Launching a command prompt as Administrator
* Activate your Python virtual environment, if needed.
* `python venv\Scripts\pywin32_postinstall.py -install`

Replace `venv` above with the path to your Python installation. 

* Then, in a regular non-admin command prompt, activate your Python and try this:
* `python -c "from win32com.shell import shellcon"`

If that throws an error, the PyWin32 installation was not successful. Try removing it from pip
and reinstalling it under the Admin command prompt, and then run the postinstall script again.

## Credits

This program was originally written by Preston Landers and is provided courtesy of 
[Journyx, Inc.](https://www.journyx.com)

## License

See the [LICENSE file](LICENSE)
