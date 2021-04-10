from os import remove, getcwd
from unittest import TestCase, main
from unittest.mock import patch, call

from package_database_mgr import PackageDatabaseMgr
from utils import Utils

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
        self.mgr = PackageDatabaseMgr()

    def tearDown(self):
        """
        Suite teardown

        """

    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_first_update_with_single_repo(self, listener_mock, git_mock):
        """
        GIVEN packages dir is empty and the mirrors.csv file contains only one
              repo.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the correct
              branch and the events must be issued to the view.
        """
        repo_name = 'bar'
        repo_url = f'https://github.com/foo/{repo_name}.git'
        branch_name = 'master'

        with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
            mirrors.write(f'{branch_name},{repo_url}')

        self.mgr.update(listener_mock)

        self.assertEqual(getcwd(), '/var/db/gbpm')

        listener_mock.on_update_start.assert_called_once()
        listener_mock.on_repo_update_start.assert_called_once_with(
            repo_name,
            branch_name
        )
        git_mock.clone_from.assert_called_once() # TODO: match the parameters!
        listener_mock.on_repo_update_finish.assert_called_once_with(
            repo_name,
            branch_name
        )
        listener_mock.on_update_finish.assert_called_once()

    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_first_update_with_multiple_repos(self, listener_mock, git_mock):
        """
        GIVEN packages dir is empty and the mirrors.csv file contains multiple
              repos.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the correct
              branch and the events must be issued to the view.
        """
        #repo_names = ['bar', 'foo', 'qux']
        #repo_urls = [
        #    'https://github.com/user/{}.git'.format(repo_names[0]),
        #    'https://github.com/user/{}.git'.format(repo_names[1]),
        #    'https://github.com/user/{}.git'.format(repo_names[2])
        #]
        #branch_name = 'master'

        #with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
        #    mirrors.truncate(0)

        #    for i in range(len(repo_urls)):
        #        mirrors.write('{},{}\n'.format(branch_name, repo_urls[i]))

        #self.mgr.update(listener_mock)

        #self.assertEqual(getcwd(), '/var/db/gbpm')

        #listener_mock.on_update_start.assert_called_once()
        #listener_mock.on_repo_update_start.assert_called_once_with(
        #    repo_names[0],
        #    branch_name
        #)
        ##git_mock.Repo.clone_from.assert_called_once_with(repo_url, repo_name, branch=branch_name)
        #listener_mock.on_repo_update_finish.assert_called_once_with(
        #    repo_names[0],
        #    branch_name
        #)
        #listener_mock.on_repo_update_start.assert_called_once_with(
        #    repo_names[1],
        #    branch_name
        #)
        #listener_mock.on_repo_update_finish.assert_called_once_with(
        #    repo_names[1],
        #    branch_name
        #)
        #listener_mock.on_repo_update_start.assert_called_once_with(
        #    repo_names[2],
        #    branch_name
        #)
        #listener_mock.on_repo_update_finish.assert_called_once_with(
        #    repo_names[2],
        #    branch_name
        #)
        #listener_mock.on_update_finish.assert_called_once()

if __name__ == "__main__":
    basic_config(level=INFO)
    main()
