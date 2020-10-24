from argparse import ArgumentParser
from sys import argv

from actions import AddPkgRepositoryAction

def main():
    """
    Main routine of gbpm

    """
    try:
        parser = ArgumentParser(
            prog='gbpm',
            description=
                'gbpm (git-based package manager) is a generic package manager '
                + 'based on git repositories, heavily inspired by vim-plug. '
                + 'For more informations, please refer the official documentation '
                + 'available at: github.com/carvalhudo/gbpm/doc (TODO)'
        )

        # The mirrors file contains a list of package repositories which will
        # be used during the 'update' operation. Such file has the same goal
        # of 'sources.list' of 'apt' package manager
        parser.add_argument(
            '-a',
            '--add-pkg-repository',
            metavar='repo-url',
            type=str,
            help='add a pkg repository to the gbpm mirror list',
            action=AddPkgRepositoryAction
        )

        # no arguments were provided
        if len(argv) == 1:
            parser.print_help()

        parser.parse_args()
    except PermissionError:
        print('you must to run with root privilegies!')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
