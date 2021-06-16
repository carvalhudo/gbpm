from json import dump, load
from os import chdir
from os.path import isdir, isfile

class PackageDatabaseMgr:

    """
    Implementation of the class responsible for the management of the package
    database.

    """

    def __init__(self):
        """
        Initialize the package database mgr data.

        """
        self.pkg_dir = "/var/db/gur/"
        self.db_file = "pkg_db.json"

        if not isdir(self.pkg_dir):
            raise RuntimeError(
                "the package dir '{}' was not found!".format(
                    self.pkg_dir
                )
            )

        db_file_path = '{}/{}'.format(self.pkg_dir, self.db_file)
        if not isfile(db_file_path):
            with open(db_file_path, 'w') as f:
                dump([], f)

    def add_entry(self, pkg_name, head_commit):
        """
        Add a new package entry into the package database.

        :pkg_name: Name of the package.
        :head_commit: Hash of the head commit of the package.

        """
        with open(self.db_file, 'r+') as f:
            pkg_entry = {
                'name': pkg_name,
                'rev': { 'remote': head_commit, 'local': '' }
            }

            curr_content = load(f)
            curr_content.append(pkg_entry)

            f.seek(0)

            dump(curr_content, f)

    def update_entry(self, pkg_name, head_commit):
        """
        Update an existing package entry in the package database.

        :pkg_name: Name of the package.
        :head_commit: Hash of the head commit of the package.

        """
        with open(self.db_file, 'r+') as f:
            curr_content = load(f)

            for entry in curr_content:
                if entry['name'] == pkg_name:
                    entry['rev']['remote'] = head_commit
                    f.seek(0)
                    dump(curr_content, f)

    def switch_dir(self):
        """
        Switch the current directory to the package directory.

        """
        chdir(self.pkg_dir)

    def is_pkg_installed(self, pkg_name):
        """
        Verify if a given package is installed.

        :pkg_name: Name of the package.
        :returns: True if the package is installed; otherwise False.

        """
        with open(self.db_file, 'r') as f:
            curr_content = load(f)

            for entry in curr_content:
                if entry['name'] == pkg_name and entry['rev']['local']:
                    return True


        return False
