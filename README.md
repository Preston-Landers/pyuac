# PyUAC - Python User Access Control

This package provides a way to invoke User Access Control (UAC) in Windows from Python.

This allows a Python process to re-spawn a new process with Administrator level rights using
the UAC prompt. Note that the original process is not elevated; a new process is created.

The main purpose of pyuac is to allow command line Python scripts to ensure they are run
as Administrator on Windows. There is no ability to execute only parts of a program 
as Administrator - the entire script is re-launched with the same command line. You can
also override the command line used for the admin process.

## Usage and examples

There are two basic ways to use this library. Perhaps the simplest way is to decorate your 
Python command line script's main function. The other is to directly use the `isUserAdmin`
and `runAsAdmin` functions yourself. The decorator allows you to automatically capture
the output of the Admin process and return that output string to the non-admin parent process.

See also [tests/example_usage.py](tests/example_usage.py)

### Decorator

The decorator is an easy way to ensure your script's main() function will respawn itself
as Admin if necessary.

#### Decorator usage example

```python
from pyuac import main_requires_admin

@main_requires_admin
def main():
    print("Do stuff here that requires being run as an admin.")
    # The window will disappear as soon as the program exits!
    input("Press enter to close the window. >")

if __name__ == "__main__":
    main()
```

#### Capture stdout from admin process

You can also capture the stdout and stderr of your Admin sub-process if you need to check
it for errors from the non-admin parent. By default, unless you set scan_for_error=False on
the decorator, it will check the last line of both stdout and stderr for the words 'error'
or 'exception', and if it finds those, will raise RuntimeError on the parent non-admin side.

```python
from pyuac import main_requires_admin

@main_requires_admin(return_output=True)
def main():
    print("Do stuff here that requires being run as an admin.")
    # The window will disappear as soon as the program exits!
    input("Press enter to close the window. >")

if __name__ == "__main__":
    rv = main()
    if not rv:
        print("I must have already been Admin!")
    else:
        admin_stdout, admin_str, *_ = rv
        if "Do stuff" in admin_stdout:
            print("It worked.")
```

### Direct usage

There are two main direct usage functions provided:

    isUserAdmin()
This returns a boolean to indicate whether the current user has elevated Administrator status.

    runAsAdmin()
Re-launch the current process (or the given command line) as an Administrator. 
This will trigger the UAC (User Access Control) prompt if necessary.

#### Direct usage example

This shows a typical usage pattern:

```python
import pyuac

def main():
    print("Do stuff here that requires being run as an admin.")
    # The window will disappear as soon as the program exits!
    input("Press enter to close the window. >")

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:        
        main()  # Already an admin here.
```

## Requirements

* This package only supports Windows at the moment. The isUserAdmin function will work under
  Linux / Posix, but the runAsAdmin functionality is currently Windows only.
  
* This requires Python 2.7, or Python 3.3 or higher.

* This requires the [PyWin32](https://pypi.org/project/pywin32/) package to be installed.

https://pypi.org/project/pywin32/
https://github.com/mhammond/pywin32

* It also depends on the packages [decorator](https://pypi.org/project/decorator/) 
and [tee](https://pypi.org/project/tee/)

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

If all else fails, and you are using a system-installed Python (not a virtualenv) then you
can try downloading the PyWin32 .exe installer.

## Changelog

See [CHANGELOG.md](CHANGELOG.md)

## Credits

This program was originally written by Preston Landers and is provided courtesy of 
[Journyx, Inc.](https://www.journyx.com)

## License

See the [LICENSE file](LICENSE)
