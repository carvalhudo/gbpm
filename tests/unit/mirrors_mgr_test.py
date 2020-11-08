from os import remove
from unittest import TestCase, main

from app.mirrors_mgr import MirrorsMgr
from logging import basicConfig as basic_config
from logging import INFO, info

class MirrorsMgrTest(TestCase):

    """
    Implementation of unit tests for mirrors manager

    """

    def setUp(self):
        """
        Suite setup

        """
        self.mgr = MirrorsMgr()

    def tearDown(self):
        """
        Suite teardown

        """
        # clear the mirrors file at the end of each testcase
        for mirror in self.mgr.get_mirrors():
            self.mgr.del_repo(mirror)

    def add_single_repo_test(self):
        """
        GIVEN the mirrors file is initially empty.
        WHEN  the user add a pkg repository using the mirrors mgr.
        THEN  the mirrors file must contain the given repository url.
        """
        repo_url = 'foo'

        self.mgr.add_repo(repo_url)
        mirrors = self.mgr.get_mirrors()

        assert repo_url in mirrors
        assert len(mirrors) == 1

    def add_multiple_repo_test(self):
        """
        GIVEN the mirrors file is intially empty.
        WHEN  the user add multiple pkg repository using the mirrors mgr.
        THEN  the mirrors file must contain all the added repositories.
        """
        repo_urls = ['foo', 'bar', 'baz', 'qux']

        for entry in repo_urls:
            self.mgr.add_repo(entry)

        mirrors = self.mgr.get_mirrors()
        for entry in repo_urls:
            assert entry in mirrors

        assert len(mirrors) == len(repo_urls)

    def add_existent_repo_test(self):
        """
        GIVEN the mirrors file is intially empty.
        WHEN  the user add a pkg repository which already exist on mirrors file,
              using the mirrors mgr.
        THEN  the mirrors file must contain only one line related to the given
              repository url.
        """
        repo_url = 'foo'

        self.mgr.add_repo(repo_url)
        mirrors = self.mgr.get_mirrors()

        assert repo_url in mirrors
        assert len(mirrors) == 1

        self.mgr.add_repo(repo_url)
        mirrors = self.mgr.get_mirrors()

        assert repo_url in mirrors
        assert len(mirrors) == 1

    def del_single_existent_repo_test(self):
        """
        GIVEN the mirrors file contains a single package repository.
        WHEN  the user delete a repository which already exist from mirrors file,
              using the mirrors mgr.
        THEN  the mirrors file must be empty.
        """
        repo_url = 'foo'

        self.mgr.add_repo(repo_url)
        mirrors = self.mgr.get_mirrors()

        assert repo_url in mirrors
        assert len(mirrors) == 1

        self.mgr.del_repo(repo_url)
        mirrors = self.mgr.get_mirrors()

        assert repo_url not in mirrors
        assert len(mirrors) == 0

    def del_single_repo_from_file_containing_multiple_test(self):
        """
        GIVEN the mirrors file contains multiple package repository.
        WHEN  the user delete a single repository which already exist from mirrors file,
              using the mirrors mgr.
        THEN  the mirrors file must contain only the another entries.
        """
        repo_urls = ['foo', 'bar', 'baz', 'qux']

        for repo in repo_urls:
            self.mgr.add_repo(repo)

        mirrors = self.mgr.get_mirrors()

        for repo in repo_urls:
            assert repo in mirrors

        assert len(mirrors) == len(repo_urls)

        self.mgr.del_repo(repo_urls[0])
        mirrors = self.mgr.get_mirrors()

        assert repo[0] not in mirrors
        assert len(mirrors) == (len(repo_urls) - 1)

        for repo in repo_urls[1:]:
            assert repo in mirrors

    def del_repo_from_empty_mirrors_file_test(self):
        """
        GIVEN the mirrors file is empty.
        WHEN  the user try to delete a repository from an empty mirrors file,
              using the mirrors mgr.
        THEN  a 'RuntimeError' exception must be raised.
        """
        repo_url = 'foo'
        exception = None

        try:
            self.mgr.del_repo(repo_url)
        except Exception as e:
            exception = e

        assert exception != None
        assert isinstance(exception, RuntimeError) == True

if __name__ == "__main__":
    basic_config(level=INFO)
    main()
