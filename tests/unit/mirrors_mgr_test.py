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

        # create the 'mirrors' file
        with open(self.mgr.mirrors_file, 'w'):
            pass

    def tearDown(self):
        """
        Suite teardown

        """
        # clear the mirrors file
        with open(self.mgr.mirrors_file, 'w') as mirrors_file:
            mirrors_file.truncate(0)

    def add_single_repo_test(self):
        """
        GIVEN the mirrors file is initially empty.
        WHEN  the user add a pkg repository using the mirrors mgr.
        THEN  the mirrors file must contain the given repository url.
        """
        repo_url = 'https://github.com/foo/foo.git'
        branch = 'master'

        self.mgr.add_repo(repo_url, branch)
        with open(self.mgr.mirrors_file, 'r') as mirrors_file:
            mirrors_content = mirrors_file.readlines()

            assert f'{branch}:{repo_url}\n' in mirrors_content
            assert len(mirrors_content) == 1

    def add_multiple_repo_test(self):
        """
        GIVEN the mirrors file is intially empty.
        WHEN  the user add multiple pkg repository using the mirrors mgr.
        THEN  the mirrors file must contain all the added repositories.
        """
        branch = 'master'
        repo_urls = [
            'https://github.com/foo/foo.git',
            'https://github.com/bar/bar.git',
            'https://github.com/baz/baz.git',
            'https://github.com/qux/qux.git'
        ]

        for entry in repo_urls:
            self.mgr.add_repo(entry, branch)

        with open(self.mgr.mirrors_file, 'r') as mirrors_file:
            mirrors_content = mirrors_file.readlines()

            for entry in repo_urls:
                assert f'{branch}:{entry}\n' in mirrors_content

            assert len(mirrors_content) == len(repo_urls)

    def add_existent_repo_test(self):
        """
        GIVEN the mirrors file is intially empty.
        WHEN  the user add a pkg repository which already exist on mirrors file,
              using the mirrors mgr.
        THEN  the mirrors file must contain only one line related to the given
              repository url.
        """
        repo_url = 'https://github.com/foo/foo.git',
        branch = 'master'

        self.mgr.add_repo(repo_url, branch)
        with open(self.mgr.mirrors_file, 'r') as mirrors_file:
            mirrors_content = mirrors_file.readlines()

            assert f'{branch}:{repo_url}\n' in mirrors_content
            assert len(mirrors_content) == 1

            self.mgr.add_repo(repo_url, branch)

            mirrors_file.seek(0)
            mirrors_content = mirrors_file.readlines()

            assert f'{branch}:{repo_url}\n' in mirrors_content
            assert len(mirrors_content) == 1

    def add_repo_with_different_branch_test(self):
        """
        GIVEN the mirrors file is intially empty.
        WHEN  the user add a pkg repository which already exist on mirrors file
              specifying a different branch, using the mirrors mgr.
        THEN  the mirrors file must contain the both entries with different branches.
        """
        repo_url = 'https://github.com/foo/foo.git'
        branches = [
            'master',
            'develop',
            'foo'
        ]

        for branch in branches:
            self.mgr.add_repo(repo_url, branch)

        with open(self.mgr.mirrors_file, 'r') as mirrors_file:
            mirrors_content = mirrors_file.readlines()

            for branch in branches:
                assert f'{branch}:{repo_url}\n' in mirrors_content

            assert len(mirrors_content) == len(branches)

    def del_single_existent_repo_test(self):
        """
        GIVEN the mirrors file contains a single package repository.
        WHEN  the user delete a repository which already exist from mirrors file,
              using the mirrors mgr.
        THEN  the mirrors file must be empty.
        """
        repo_url = 'https://github.com/foo/foo.git',
        branch = 'master'

        self.mgr.add_repo(repo_url, branch)
        with open(self.mgr.mirrors_file, 'r') as mirrors_file:
            mirrors_content = mirrors_file.readlines()

            assert f'{branch}:{repo_url}\n' in mirrors_content
            assert len(mirrors_content) == 1

            self.mgr.del_repo(repo_url, branch)

            mirrors_file.seek(0)
            mirrors_content = mirrors_file.readlines()

            assert f'{branch}:{repo_url}\n' not in mirrors_content
            assert len(mirrors_content) == 0

    def del_single_repo_from_file_containing_multiple_test(self):
        """
        GIVEN the mirrors file contains multiple package repository.
        WHEN  the user delete a single repository which already exist from mirrors file,
              using the mirrors mgr.
        THEN  the mirrors file must contain only the another entries.
        """
        branch = 'master'
        repo_urls = [
            'https://github.com/foo/foo.git',
            'https://github.com/bar/bar.git',
            'https://github.com/baz/baz.git',
            'https://github.com/qux/qux.git'
        ]

        for repo in repo_urls:
            self.mgr.add_repo(repo, branch)

        with open(self.mgr.mirrors_file, 'r') as mirrors_file:
            mirrors_content = mirrors_file.readlines()

            for repo in repo_urls:
                assert f'{branch}:{repo}\n' in mirrors_content

            assert len(mirrors_content) == len(repo_urls)

            self.mgr.del_repo(repo_urls[0], branch)

            mirrors_file.seek(0)
            mirrors_content = mirrors_file.readlines()

            assert f'{branch}:{repo[0]}\n' not in mirrors_content
            assert len(mirrors_content) == (len(repo_urls) - 1)

            for repo in repo_urls[1:]:
                assert f'{branch}:{repo}\n' in mirrors_content

    def del_single_repo_from_file_containing_the_same_repo_with_different_branches_test(self):
        """
        GIVEN the mirrors file contains multiple definitions of the same repository
              with different branches.
        WHEN  the user delete a single repository from mirrors file, using the mirrors
              mgr.
        THEN  the mirrors file must contain only the another entries.
        """
        repo_url = 'https://github.com/foo/foo.git'
        branches = [
            'master',
            'develop',
            'foo'
        ]

        for branch in branches:
            self.mgr.add_repo(repo_url, branch)

        with open(self.mgr.mirrors_file, 'r') as mirrors_file:
            mirrors_content = mirrors_file.readlines()

            for branch in branches:
                assert f'{branch}:{repo_url}\n' in mirrors_content

            assert len(mirrors_content) == len(branches)

            self.mgr.del_repo(repo_url, branches[1])

            mirrors_file.seek(0)
            mirrors_content = mirrors_file.readlines()

            del branches[1]
            for branch in branches:
                assert f'{branch}:{repo_url}\n' in mirrors_content

            assert len(mirrors_content) == len(branches)

    def del_repo_from_empty_mirrors_file_test(self):
        """
        GIVEN the mirrors file is empty.
        WHEN  the user try to delete a repository from an empty mirrors file,
              using the mirrors mgr.
        THEN  a 'RuntimeError' exception must be raised.
        """
        repo_url = 'foo'
        branch = 'master'
        exception = None

        try:
            self.mgr.del_repo(repo_url, branch)
        except Exception as e:
            exception = e

        assert exception != None
        assert isinstance(exception, RuntimeError) == True

if __name__ == "__main__":
    basic_config(level=INFO)
    main()
