#!/usr/bin/env python

"""
Example demonstrating usage of pyuac, which demonstrates handled quoted strings as
script command line parameters. Invoke this like:

> python example_usage.py 3 4 --sum --string1 "Here's \"quotes\" in a string!"
"""

from pyuac.decorator import main_requires_admin


@main_requires_admin
def main():
    """
    Some example code; your program here.
    """
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        'integers', metavar='N', type=int, nargs='+',
        help='an integer for the accumulator')
    parser.add_argument(
        '--sum', dest='accumulate', action='store_const',
        const=sum, default=max,
        help='sum the integers (default: find the max)')
    parser.add_argument(
        '--string1', dest='string1', action='store',
        default=None,
        help='Extra string to emit.')
    parser.add_argument(
        '--string2', dest='string2', action='store',
        default=None,
        help='Another extra string to emit.')

    args = parser.parse_args()
    print(args.accumulate(args.integers))

    string1 = args.string1
    string2 = args.string2
    if string1 is not None or string2 is not None:
        print("String 1: %r" % (string1,))
        print("String 2: %r" % (string2,))

    input("\nPress enter to quit. >")


if __name__ == '__main__':
    # Invoke your decorated main function like normal
    rv = main()
