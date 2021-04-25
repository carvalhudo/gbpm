from unittest import TestCase, main
from unittest.mock import patch

#from package_database_mgr import PackageDatabaseMgr

from logging import basicConfig as basic_config
from logging import INFO, info

class PackageDatabaseMgrTest(TestCase):

    """
    Implementation of unit tests for mirrors manager

    """

    def setUp(self):
        """
        Suite setup

        """
        #self.mgr = PackageDatabaseMgr()
        # TODO: create mocked package dir

    def tearDown(self):
        """
        Suite teardown

        """
        # TODO: remove mocked package dir

    @patch('git.Repo')
    def test_add_single_entry(self, git_mock):
        """
        GIVEN the package database is initially empty.
        WHEN  we add a new entry into it.
        THEN  the package database must contain the entry with their respective
              properties.
        """
        pass

    @patch('git.Repo')
    def test_add_multiple_entry(self, git_mock):
        """
        GIVEN the package database is initially empty.
        WHEN  we add a new entry into it.
        THEN  the package database must contain the entry with their respective
              properties.
        """
        pass

    @patch('git.Repo')
    def test_update_single_entry(self, git_mock):
        """
        GIVEN packages dir is empty and the mirrors.csv file contains only one
              repo.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the correct
              branch and the events must be issued to the view.
        """
        pass

    @patch('git.Repo')
    def test_update_multiple_entry(self, git_mock):
        """
        GIVEN packages dir is empty and the mirrors.csv file contains only one
              repo.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the correct
              branch and the events must be issued to the view.
        """
        pass

if __name__ == "__main__":
    basic_config(level=INFO)
    main()
