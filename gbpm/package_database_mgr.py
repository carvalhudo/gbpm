from os import chdir
from os.path import isdir, isfile
from json import load, dump

import git

class PackageDatabaseMgr:

    """
    Docstring for PackageDatabaseMgr.

    """

    def __init__(self):
        """
        TODO: to be defined.

        """
        self.pkg_dir = "/var/db/gbpm/"
        #self.pkg_dir = "db/"
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

    def add_entry(self, entry, base_repo):
        """
        TODO: Docstring for init_db.

        :arg1: TODO
        :returns: TODO

        """
        desc_file = '{}/{}/pkg_desc.json'.format(base_repo, entry)
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
            entry
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

    def update_entry(self, entry, base_repo):
        """TODO: Docstring for update_db.

        :arg1: TODO
        :returns: TODO

        """
        desc_file = '{}/{}/pkg_desc.json'.format(base_repo, entry)
        pkg = ''
        branch = ''

        with open(desc_file, 'r') as pkg_desc:
            pkg_desc_content = load(pkg_desc)

            pkg = pkg_desc_content['name']
            branch = pkg_desc_content['branch']

        pkg_dir = '{}/{}/.repo'.format(
            base_repo,
            entry
        )

        pkg_repo = git.Repo(pkg_dir)
        pkg_repo.remotes.origin.fetch()

        remote_hash = ''
        with open('{}/.git/refs/remotes/origin/{}'.format(pkg_dir, branch), 'r') as f:
            remote_hash = f.read().replace('\n', '')

        with open(self.db_file, 'r+') as f:
            curr_content = load(f)

            for pkg_entry in curr_content:
                if pkg_entry['name'] == pkg:
                    pkg_entry['remote'] = remote_hash
                    f.seek(0)
                    dump(curr_content, f)

    def switch_dir(self):
        """TODO: Docstring for switch_dir.
        :returns: TODO

        """
        chdir(self.pkg_dir)
