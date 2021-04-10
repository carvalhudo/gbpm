from sys import argv
from argparse import ArgumentParser

from views import CliUpdateView

def run(args):
    """
    Main routine of gbpm.

    """
    if args.update:
        view = CliUpdateView()
        view.update()

def parse_args():
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
        help='update the local package database',
        action='store_true'
    )

    # no arguments were provided
    if len(argv) == 1:
        parser.print_help()

    return parser.parse_args()

if __name__ == '__main__':
    try:
        args = parse_args()

        run(args)
    except Exception as e:
        print(e)
