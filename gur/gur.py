from argparse import ArgumentParser, RawTextHelpFormatter
from sys import argv, exit

from app import App

def parse_args(): # pragma: no cover
    """
    Parse the command line arguments.

    """
    banner = """
     ____ _   _ ____
    / ___| | | |  _ \\
   | |  _| | | | |_) |
   | |_| | |_| |  _ <
    \____|\___/|_| \_\\
 (g)it(u)ser(r)epository"""

    parser = ArgumentParser(
        prog='gur',
        description=banner,
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        '-u',
        '--update',
        help='sync the local package database',
        action='store_true'
    )

    parser.add_argument(
        '-l',
        '--list-pkgs',
        help='list the available packages',
        action='store_true'
    )

    # no arguments were provided
    if len(argv) == 1:
        parser.print_help()

    return parser.parse_args()

if __name__ == '__main__': # pragma: no cover
    try:
        args = parse_args()
        app = App(args)

        app.run()
    except Exception as err:
        print(err)
        exit(1)
