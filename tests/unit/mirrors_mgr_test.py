from os import remove
from unittest import TestCase, main

from app.mirrors_mgr import MirrorsMgr

class ConfigMgrTest(TestCase):

    """
    Implementation of unit tests for config manager

    """

    def setUp(self):
        """
        Suite setup

        """
        self.mgr = MirrorsMgr()

        # create the 'mirrors' file
        with open(self.mgr.mirrors_file, 'w'):
            pass

    def tearDown(self):
        """
        Suite teardown

        """
        remove(self.mgr.mirrors_file)

    def add_single_repo_test(self):
        """
        GIVEN the mirrors file is initially empty.
        WHEN  the user add a pkg repository using the config mgr.
        THEN  the mirrors file must contain the given repository url.
        """
        repo_url = 'foo'

        self.mgr.add_repo(repo_url)
        with open(self.mgr.mirrors_file, 'r') as mirrors_file:
            mirrors_content = mirrors_file.readlines()

            assert f'{repo_url}\n' in mirrors_content
            assert len(mirrors_content) == 1

    def add_multiple_repo_test(self):
        """
        GIVEN the mirrors file is intially empty.
        WHEN  the user add multiple pkg repository using the config mgr.
        THEN  the mirrors file must contain all the added repositories.
        """
        repo_urls = ['foo', 'bar', 'baz', 'qux']

        for entry in repo_urls:
            self.mgr.add_repo(entry)

        with open(self.mgr.mirrors_file, 'r') as mirrors_file:
            mirrors_content = mirrors_file.readlines()

            for entry in repo_urls:
                assert f'{entry}\n' in mirrors_content

            assert len(mirrors_content) == len(repo_urls)

    def add_existent_repo_test(self):
        """
        GIVEN the mirrors file is intially empty.
        WHEN  the user add a pkg repository which already exist on mirrors file,
              using the config mgr
        THEN  the mirrors file must contain only one line related to the given
              repository url.
        """
        repo_url = 'foo'

        self.mgr.add_repo(repo_url)
        with open(self.mgr.mirrors_file, 'r') as mirrors_file:
            mirrors_content = mirrors_file.readlines()

            assert f'{repo_url}\n' in mirrors_content
            assert len(mirrors_content) == 1

            self.mgr.add_repo(repo_url)

            mirrors_file.seek(0)
            mirrors_content = mirrors_file.readlines()

            assert f'{repo_url}\n' in mirrors_content
            assert len(mirrors_content) == 1

if __name__ == "__main__":
    main()
