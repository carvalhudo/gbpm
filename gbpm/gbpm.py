from argparse import ArgumentParser
from sys import argv

from app import App

def parse_args(): # pragma: no cover
    """
    Parse the command line arguments.

    """
    parser = ArgumentParser(
        prog='gbpm',
        description=
            'gbpm (git-based package manager) is a generic package manager '
            + 'based on git repositories.'
    )

    parser.add_argument(
        '-u',
        '--update',
        help='sync the local package database',
        action='store_true'
    )

    # no arguments were provided
    if len(argv) == 1:
        parser.print_help()

    return parser.parse_args()

if __name__ == '__main__':
    try:
        args = parse_args()
        app = App(args)

        app.run()
    except Exception as e:
        print(e)
