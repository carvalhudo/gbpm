from os import listdir, chdir
from os.path import isdir, isfile
from json import dump
from getpass import getpass
from git import Repo

from mirrors_mgr import MirrorsMgr
from git_apps.git_app_factory import GitAppFactory
from git_apps.errors.app_not_supported_error import AppNotSupportedError
from git_apps.errors.connection_failure_error import ConnectionFailureError

class PackageDatabaseMgr:

    """
    Docstring for PackageDatabaseMgr.

    """

    def __init__(self):
        """
        TODO: to be defined.

        """
        self.__pkg_dir = "/var/db/gbpm/"
        self.__db_file = "pkg_db.json"

        if not isdir(self.__pkg_dir):
            raise RuntimeError(
                f"the package dir '{self.__pkg_dir}' was not found!"
            )

    def update(self):
        """
        TODO: Docstring for update.
        :returns: TODO

        """
        chdir(self.__pkg_dir)

        # First update operation
        if not isfile(self.__db_file):
            with open(self.__db_file, 'w') as f:
                dump([], f)

        mirrors = MirrorsMgr().get_mirrors()
        for repo in mirrors:
            try:
                git = GitAppFactory.build(repo)
                repo_name = git.get_repo_name()

                # The repository doesn't exist locally
                if not isdir(repo_name):
                    print(f'cloning {repo}')
                    git.clone()
                else:
                    print(f'updating {repo}')
                    git.pull()

                #for pkg_dir in listdir():
                #    pass
                    #pkg_entry = {
                    #    'name': pkg_dir,
                    #    'local-version': '',
                    #    'upstream-version': git.head_commit
                    #}

                # TODO: if directory is empty clone the pkg repo
                # TODO: if not, pull in each one of them and check if there's updates for each package
                # TODO: if yes, update the local database
            except AppNotSupportedError as e:
                print(e)
                continue
            except ConnectionFailureError as e:
                print(e)
