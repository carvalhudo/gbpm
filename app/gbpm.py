from sys import argv
from argparse import ArgumentParser

from actions import AddPkgRepositoryAction, DelPkgRepositoryAction

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
            help='add a pkg repository to the mirror list',
            action=AddPkgRepositoryAction
        )

        parser.add_argument(
            '-d',
            '--del-pkg-repository',
            metavar='repo-url',
            type=str,
            help='delete a pkg repository from the mirror list',
            action=DelPkgRepositoryAction
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
    except Exception as err:
        print(err)
