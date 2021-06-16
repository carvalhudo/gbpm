from unittest import TestCase, main

from os import remove, getcwd, chdir
from json import load, dump

from package_database_mgr import PackageDatabaseMgr

class PackageDatabaseMgrTest(TestCase):

    """
    Implementation of unit tests for PackageDatabaseMgr class.

    """

    def setUp(self):
        """
        Suite setup.

        """
        self.mgr = PackageDatabaseMgr()
        self.old_dir = getcwd()
        self.mgr.switch_dir()

    def tearDown(self):
        """
        Suite teardown.

        """
        remove(self.mgr.db_file)
        chdir(self.old_dir)

    def test_add_single_entry(self):
        """
        GIVEN the package database is initially empty.
        WHEN  we add a new entry to the database.
        THEN  the package database must contain the entry with their respective
              properties.

        """
        pkg_name = 'fake_pkg'
        pkg_hash = 'fake_hash'
        expected_content = [
            {
                'name': pkg_name,
                'rev': { 'remote': pkg_hash, 'local': '' }
            }
        ]

        self.mgr.add_entry(pkg_name, pkg_hash)

        with open(self.mgr.db_file, 'r') as f:
            read_content = load(f)

            self.assertEqual(read_content, expected_content)

    def test_add_multiple_entries(self):
        """
        GIVEN the package database is initially empty.
        WHEN  we add multiple entries into the database.
        THEN  the package database must contain the entries with their respective
              properties.

        """
        pkg_names = ['fake_pkg_1', 'fake_pkg_2', 'fake_pkg_3']
        pkg_hashes = ['fake_hash_1', 'fake_hash_2', 'fake_hash_3']
        expected_content = [
            {
                'name': pkg_names[0],
                'rev': { 'remote': pkg_hashes[0], 'local': '' }
            },
            {
                'name': pkg_names[1],
                'rev': { 'remote': pkg_hashes[1], 'local': '' }
            },
            {
                'name': pkg_names[2],
                'rev': { 'remote': pkg_hashes[2], 'local': '' }
            }
        ]

        self.mgr.add_entry(pkg_names[0], pkg_hashes[0])
        self.mgr.add_entry(pkg_names[1], pkg_hashes[1])
        self.mgr.add_entry(pkg_names[2], pkg_hashes[2])

        with open(self.mgr.db_file, 'r') as f:
            read_content = load(f)

            self.assertEqual(read_content, expected_content)

    def test_update_single_entry(self):
        """
        GIVEN the package dir is not empty and contains only one entry.
        WHEN  the user update an existing entry.
        THEN  the given entry must be updated with the new commit hash.

        """
        pkg_name = 'fake_pkg'
        old_pkg_hash = 'old_fake_hash'
        new_pkg_hash = 'new_fake_hash'
        expected_content = [
            {
                'name': pkg_name,
                'rev': { 'remote': new_pkg_hash, 'local': '' }
            }
        ]

        self.mgr.add_entry(pkg_name, old_pkg_hash)
        self.mgr.update_entry(pkg_name, new_pkg_hash)

        with open(self.mgr.db_file, 'r') as f:
            read_content = load(f)

            self.assertEqual(read_content, expected_content)

    def test_update_multiple_entries(self):
        """
        GIVEN the packages dir is not empty and contains multiple entries.
        WHEN  the user update multiple entries.
        THEN  the respsective entries must be update on the database with the
              new commit hashes.

        """
        pkg_names = ['fake_pkg_1', 'fake_pkg_2', 'fake_pkg_3']
        old_pkg_hashes = ['old_fake_hash_1', 'old_fake_hash_2', 'old_fake_hash_3']
        new_pkg_hashes = ['new_fake_hash_1', 'new_fake_hash_2', 'new_fake_hash_3']
        expected_content = [
            {
                'name': pkg_names[0],
                'rev': { 'remote': new_pkg_hashes[0], 'local': '' }
            },
            {
                'name': pkg_names[1],
                'rev': { 'remote': new_pkg_hashes[1], 'local': '' }
            },
            {
                'name': pkg_names[2],
                'rev': { 'remote': new_pkg_hashes[2], 'local': '' }
            }
        ]

        self.mgr.add_entry(pkg_names[0], old_pkg_hashes[0])
        self.mgr.add_entry(pkg_names[1], old_pkg_hashes[1])
        self.mgr.add_entry(pkg_names[2], old_pkg_hashes[2])

        self.mgr.update_entry(pkg_names[0], new_pkg_hashes[0])
        self.mgr.update_entry(pkg_names[1], new_pkg_hashes[1])
        self.mgr.update_entry(pkg_names[2], new_pkg_hashes[2])

        with open(self.mgr.db_file, 'r') as f:
            read_content = load(f)

            self.assertEqual(read_content, expected_content)

    def test_update_only_one_entry(self):
        """
        GIVEN the package dir is not empty and contains multiple entries.
        WHEN  the user update only one existing entry.
        THEN  the given entry must be updated with the new commit hash and the
              another ones must not be changed.

        """
        pkg_names = ['fake_pkg_1', 'fake_pkg_2', 'fake_pkg_3']
        old_pkg_hashes = ['old_fake_hash_1', 'old_fake_hash_2', 'old_fake_hash_3']
        new_pkg_hashes = ['new_fake_hash_1', 'new_fake_hash_2', 'new_fake_hash_3']
        expected_content = [
            {
                'name': pkg_names[0],
                'rev': { 'remote': old_pkg_hashes[0], 'local': '' }
            },
            {
                'name': pkg_names[1],
                'rev': { 'remote': new_pkg_hashes[1], 'local': '' }
            },
            {
                'name': pkg_names[2],
                'rev': { 'remote': old_pkg_hashes[2], 'local': '' }
            }
        ]

        self.mgr.add_entry(pkg_names[0], old_pkg_hashes[0])
        self.mgr.add_entry(pkg_names[1], old_pkg_hashes[1])
        self.mgr.add_entry(pkg_names[2], old_pkg_hashes[2])

        self.mgr.update_entry(pkg_names[1], new_pkg_hashes[1])

        with open(self.mgr.db_file, 'r') as f:
            read_content = load(f)

            self.assertEqual(read_content, expected_content)

    def test_update_non_existent_entry(self):
        """
        GIVEN the package dir is not empty and contains only one entry.
        WHEN  the user try to update a non existing entry.
        THEN  no changes will be commited into the database.

        """
        pkg_name = 'fake_pkg'
        pkg_hash = 'old_fake_hash'
        expected_content = [
            {
                'name': pkg_name,
                'rev': { 'remote': pkg_hash, 'local': '' }
            }
        ]

        self.mgr.add_entry(pkg_name, pkg_hash)
        self.mgr.update_entry('non_existing_package', 'fake_hash')

        with open(self.mgr.db_file, 'r') as f:
            read_content = load(f)

            self.assertEqual(read_content, expected_content)

    def test_is_installed_with_non_installed_pkg(self):
        """
        GIVEN the specified package is not installed.
        WHEN  the user issues an in_pkg_installed call for this package.
        THEN  the return must be False.

        """
        pkg_name = 'fake_pkg'
        pkg_hash = 'old_fake_hash'

        self.mgr.add_entry(pkg_name, pkg_hash)
        self.assertFalse(self.mgr.is_pkg_installed(pkg_name))

    def test_is_installed_with_installed_pkg(self):
        """
        GIVEN the specified package is installed.
        WHEN  the user issues an in_pkg_installed call for this package.
        THEN  the return must be True.

        """
        pkg_name = 'fake_pkg'
        remote_pkg_hash = 'remote_fake_hash'
        local_pkg_hash = 'local_fake_hash'

        self.mgr.add_entry(pkg_name, remote_pkg_hash)

        # simulate a package installation at database level.
        with open(self.mgr.db_file, 'r+') as f:
            curr_content = load(f)

            for entry in curr_content:
                if entry['name'] == pkg_name:
                    entry['rev']['local'] = local_pkg_hash
                    f.seek(0)
                    dump(curr_content, f)

        self.assertTrue(self.mgr.is_pkg_installed(pkg_name))

    def test_is_installed_with_non_existing_pkg(self):
        """
        GIVEN the specified package doesn't exist on database.
        WHEN  the user issues an in_pkg_installed call for this package.
        THEN  the return must be False.

        """
        pkg_name = 'fake_pkg'

        self.assertFalse(self.mgr.is_pkg_installed(pkg_name))

if __name__ == "__main__":
    main()
