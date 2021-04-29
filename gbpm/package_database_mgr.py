from os import chdir
from os.path import isdir, isfile
from json import load, dump

import git

class PackageDatabaseMgr:

    """
    Class responsible for the management of package database.

    """

    def __init__(self):
        self.pkg_dir = "/var/db/gbpm/"
        self.db_file = "pkg_db.json"

        if not isdir(self.pkg_dir):
            raise RuntimeError(
                "the package dir '{}' was not found!".format(
                    self.pkg_dir
                )
            )

        if not isfile(self.db_file):
            with open(self.db_file, 'w') as f:
                dump([], f)

    def add_entry(self, pkg_entry, base_repo):
        """
        Add a new package entry into the package database.

        :pkg_entry: Name of the package to be added to the database.
        :base_repo: Package repository name.

        """
        desc_file = '{}/{}/pkg_desc.json'.format(base_repo, pkg_entry)
        pkg = ''
        repo = ''
        branch = ''

        with open(desc_file, 'r') as pkg_desc:
            pkg_desc_content = load(pkg_desc)

            pkg = pkg_desc_content['name']
            repo = pkg_desc_content['repo']
            branch = pkg_desc_content['branch']

        pkg_dir = '{}/{}/.repo'.format(
            base_repo,
            pkg_entry
        )

        pkg_repo = git.Repo.init(pkg_dir)
        origin = pkg_repo.create_remote(
            'origin',
            repo
        )
        origin.fetch()

        remote_hash = ''
        with open('{}/.git/refs/remotes/origin/{}'.format(pkg_dir, branch), 'r') as f:
            remote_hash = f.read().replace('\n', '')

        with open(self.db_file, 'r+') as f:
            pkg_entry = {
                pkg: { 'remote': remote_hash, 'local': '' }
            }

            curr_content = load(f)
            curr_content.append(pkg_entry)

            f.seek(0)

            dump(curr_content, f)

    def update_entry(self, pkg_entry, base_repo):
        """
        Update an existing package entry in the package database.

        :pkg_entry: Name of the package to be added to the database.
        :base_repo: Package repository name.

        """
        desc_file = '{}/{}/pkg_desc.json'.format(base_repo, pkg_entry)
        pkg = ''
        branch = ''

        with open(desc_file, 'r') as pkg_desc:
            pkg_desc_content = load(pkg_desc)

            pkg = pkg_desc_content['name']
            branch = pkg_desc_content['branch']

        pkg_dir = '{}/{}/.repo'.format(
            base_repo,
            pkg_entry
        )

        pkg_repo = git.Repo(pkg_dir)
        pkg_repo.remotes.origin.fetch()

        remote_hash = ''
        with open('{}/.git/refs/remotes/origin/{}'.format(pkg_dir, branch), 'r') as f:
            remote_hash = f.read().replace('\n', '')

        with open(self.db_file, 'r+') as f:
            curr_content = load(f)

            for entry in curr_content:
                if entry['name'] == pkg:
                    entry['remote'] = remote_hash
                    f.seek(0)
                    dump(curr_content, f)

    def switch_dir(self):
        """
        Switch the current directory to the package directory.

        """
        chdir(self.pkg_dir)
