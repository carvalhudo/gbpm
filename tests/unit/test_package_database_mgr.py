from unittest import TestCase, main

from os import remove, getcwd, chdir
from json import load

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
        WHEN  we add a new entry to it.
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

    def test_add_multiple_entry(self):
        """
        GIVEN the package database is initially empty.
        WHEN  we add multiple entries into it.
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

    def test_update_multiple_entry(self):
        """
        GIVEN the packages dir is not empty and contains multiple entries.
        WHEN  the user update multiple entries.
        THEN  the respsective entries must be update on the database with the
              new commit hash.

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
        WHEN  the user update an existing entry.
        THEN  the given entry must be updated with the new commit hash.

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

        # TODO: update with non existing package.

if __name__ == "__main__":
    main()
