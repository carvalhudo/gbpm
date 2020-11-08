from sys import argv
from argparse import ArgumentParser

from actions import (
    UpdateAction
)

def main():
    """
    Main routine of gbpm

    """
    try:
        parser = ArgumentParser(
            prog='gbpm',
            description=
                'gbpm (git-based package manager) is a generic package manager '
                + 'based on git repositories.'
        )

        parser.add_argument(
            '-u',
            '--update',
            metavar='',
            help='update the local package database',
            action=UpdateAction
        )

        # no arguments were provided
        if len(argv) == 1:
            parser.print_help()

        parser.parse_args()
    except PermissionError:
        print('Error: you must to run with root privilegies.')
    except ValueError as err:
        parser.print_help()

if __name__ == '__main__':
    main()
