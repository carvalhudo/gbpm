from unittest import TestCase, main
from unittest.mock import patch, call, ANY

from logging import basicConfig as basic_config
from logging import INFO

from commands import UpdateCmd

class UpdateTest(TestCase):

    """
    Implementation of unit tests for update command.

    """

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_first_update_with_single_repo_and_single_package(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN the package dir is empty, the mirrors.csv file contains only one
              repo which contains only one package.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the correct
              branch, the package must be added into the package database and
              the events must be issued to the view properly.

        """
        repo_name = 'bar-repo'
        repo_url = 'https://github.com/foo/{}.git'.format(repo_name)
        branch_name = 'master'

        with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
            mirrors.write('{},{}'.format(branch_name, repo_url))

        listdir_mock.return_value = ['foo-pkg']
        isdir_mock.return_value = False

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_repo_update_start(repo_name, branch_name),
                call.on_repo_update_finish(repo_name, branch_name),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.add_entry('foo-pkg', repo_name)
            ]
        )

        git_mock.assert_has_calls(
            [
                call.clone_from(
                    repo_url,
                    repo_name,
                    branch=branch_name,
                    progress=ANY
                )
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_first_update_with_single_repo_and_multiple_packages(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN the package dir is empty, the mirrors.csv file contains only one
              repo which contains multiple packages.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the package dir in the correct
              branch, the packages must be added into the package database and
              the events must be issued to the view properly.

        """
        repo_name = 'bar-repo'
        repo_url = 'https://github.com/foo/{}.git'.format(repo_name)
        branch_name = 'master'

        with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
            mirrors.truncate(0)
            mirrors.write('{},{}'.format(branch_name, repo_url))

        listdir_mock.return_value = [
            'foo-pkg',
            'bar-pkg',
            'baz-pkg',
            'qux-pkg'
        ]
        isdir_mock.return_value = False

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_repo_update_start(repo_name, branch_name),
                call.on_repo_update_finish(repo_name, branch_name),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.add_entry('foo-pkg', repo_name),
                call.add_entry('bar-pkg', repo_name),
                call.add_entry('baz-pkg', repo_name),
                call.add_entry('qux-pkg', repo_name)
            ],
        )

        git_mock.assert_has_calls(
            [
                call.clone_from(
                    repo_url,
                    repo_name,
                    branch=branch_name,
                    progress=ANY
                )
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_first_update_with_multiple_repos_and_single_packages(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN the package dir is empty and the mirrors.csv file contains
              multiple repos and each one of them contains only one package.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the package dir in the
              correct branch, the package must be added into the package
              database and the events must be issued to the view properly.

        """
        repo_names = ['foo-repo', 'bar-repo', 'qux-repo']
        repo_urls = [
            'https://github.com/user/{}.git'.format(repo_names[0]),
            'https://github.com/user/{}.git'.format(repo_names[1]),
            'https://github.com/user/{}.git'.format(repo_names[2])
        ]
        branch_name = 'master'

        with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
            mirrors.truncate(0)
            for i in range(len(repo_urls)):
                mirrors.write('{},{}\n'.format(branch_name, repo_urls[i]))

        listdir_mock.return_value = ['foo-pkg']
        isdir_mock.return_value = False

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_repo_update_start(repo_names[0], branch_name),
                call.on_repo_update_finish(repo_names[0], branch_name),
                call.on_repo_update_start(repo_names[1], branch_name),
                call.on_repo_update_finish(repo_names[1], branch_name),
                call.on_repo_update_start(repo_names[2], branch_name),
                call.on_repo_update_finish(repo_names[2], branch_name),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.add_entry('foo-pkg', repo_names[0]),
                call.add_entry('foo-pkg', repo_names[1]),
                call.add_entry('foo-pkg', repo_names[2]),
            ],
        )

        git_mock.assert_has_calls(
            [
                call.clone_from(
                    repo_urls[0],
                    repo_names[0],
                    branch=branch_name,
                    progress=ANY
                ),
                call.clone_from(
                    repo_urls[1],
                    repo_names[1],
                    branch=branch_name,
                    progress=ANY
                ),
                call.clone_from(
                    repo_urls[2],
                    repo_names[2],
                    branch=branch_name,
                    progress=ANY
                ),
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_first_update_with_multiple_repos_and_multiple_packages(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN the package dir is empty and the mirrors.csv file contains
              multiple repos and each one of them contains multiple packages.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the
              correct branch, the packages must be added into the package
              database and the events must be issued to the view properly.

        """
        repo_names = ['foo-repo', 'bar-repo', 'qux-repo']
        repo_urls = [
            'https://github.com/user/{}.git'.format(repo_names[0]),
            'https://github.com/user/{}.git'.format(repo_names[1]),
            'https://github.com/user/{}.git'.format(repo_names[2])
        ]
        branch_name = 'master'

        with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
            mirrors.truncate(0)
            for i in range(len(repo_urls)):
                mirrors.write('{},{}\n'.format(branch_name, repo_urls[i]))

        listdir_mock.return_value = [
            'foo-pkg',
            'bar-pkg',
            'qux-pkg'
        ]
        isdir_mock.return_value = False

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_repo_update_start(repo_names[0], branch_name),
                call.on_repo_update_finish(repo_names[0], branch_name),
                call.on_repo_update_start(repo_names[1], branch_name),
                call.on_repo_update_finish(repo_names[1], branch_name),
                call.on_repo_update_start(repo_names[2], branch_name),
                call.on_repo_update_finish(repo_names[2], branch_name),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.add_entry('foo-pkg', repo_names[0]),
                call.add_entry('bar-pkg', repo_names[0]),
                call.add_entry('qux-pkg', repo_names[0]),
                call.add_entry('foo-pkg', repo_names[1]),
                call.add_entry('bar-pkg', repo_names[1]),
                call.add_entry('qux-pkg', repo_names[1]),
                call.add_entry('foo-pkg', repo_names[2]),
                call.add_entry('bar-pkg', repo_names[2]),
                call.add_entry('qux-pkg', repo_names[2])
            ],
        )

        git_mock.assert_has_calls(
            [
                call.clone_from(
                    repo_urls[0],
                    repo_names[0],
                    branch=branch_name,
                    progress=ANY
                ),
                call.clone_from(
                    repo_urls[1],
                    repo_names[1],
                    branch=branch_name,
                    progress=ANY
                ),
                call.clone_from(
                    repo_urls[2],
                    repo_names[2],
                    branch=branch_name,
                    progress=ANY
                ),
            ]
        )

    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_first_update_with_multiple_repos_with_no_packages(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock):
        """
        GIVEN the package dir is empty and the mirrors.csv file contains
              multiple repos with no packages.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the
              correct branch, no packages must be added into the package
              database and the events must be issued to the view properly.

        """
        repo_names = ['foo-repo', 'bar-repo', 'qux-repo']
        repo_urls = [
            'https://github.com/user/{}.git'.format(repo_names[0]),
            'https://github.com/user/{}.git'.format(repo_names[1]),
            'https://github.com/user/{}.git'.format(repo_names[2])
        ]
        branch_name = 'master'

        with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
            mirrors.truncate(0)
            for i in range(len(repo_urls)):
                mirrors.write('{},{}\n'.format(branch_name, repo_urls[i]))

        listdir_mock.return_value = ['.git']

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_repo_update_start(repo_names[0], branch_name),
                call.on_repo_update_finish(repo_names[0], branch_name),
                call.on_repo_update_start(repo_names[1], branch_name),
                call.on_repo_update_finish(repo_names[1], branch_name),
                call.on_repo_update_start(repo_names[2], branch_name),
                call.on_repo_update_finish(repo_names[2], branch_name),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.switch_dir.assert_called_once()
        pkg_mgr_mock.add_entry.assert_not_called()

        git_mock.assert_has_calls(
            [
                call.clone_from(
                    repo_urls[0],
                    repo_names[0],
                    branch=branch_name,
                    progress=ANY
                ),
                call.clone_from(
                    repo_urls[1],
                    repo_names[1],
                    branch=branch_name,
                    progress=ANY
                ),
                call.clone_from(
                    repo_urls[2],
                    repo_names[2],
                    branch=branch_name,
                    progress=ANY
                ),
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_update_with_single_repo_and_single_package(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN packages dir is not empty, the mirrors.csv file contains
              only one repo and it contains only one package.
        WHEN  the user issues an update command.
        THEN  the repository must be pulled from origin, the package must
              be added into the package database and the events must be
              issued to the view properly.

        """
        repo_name = 'bar-repo'
        repo_url = 'https://github.com/foo/{}.git'.format(repo_name)
        branch_name = 'master'

        with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
            mirrors.write('{},{}'.format(branch_name, repo_url))

        listdir_mock.return_value = ['foo-pkg']
        isdir_mock.return_value = True

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_repo_update_start(repo_name, branch_name),
                call.on_update_progress(1, 0, 1, ''),
                call.on_update_progress(1, 1, 1, ''),
                call.on_repo_update_finish(repo_name, branch_name),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.update_entry('foo-pkg', repo_name)
            ]
        )

        git_mock.assert_has_calls(
            [
                call(repo_name),
                call().remotes.origin.pull(branch_name)
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_update_with_single_repo_and_multiple_packages(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN packages dir is not empty, the mirrors.csv file contains only
              one repo and it contains multiple packages.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the correct
              branch, the packages must be added into the package database and
              the events must be issued to the view properly.

        """
        repo_name = 'bar-repo'
        repo_url = 'https://github.com/foo/{}.git'.format(repo_name)
        branch_name = 'master'

        with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
            mirrors.truncate(0)
            mirrors.write('{},{}'.format(branch_name, repo_url))

        listdir_mock.return_value = [
            'foo-pkg',
            'bar-pkg',
            'baz-pkg',
            'qux-pkg'
        ]
        isdir_mock.return_value = True

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_repo_update_start(repo_name, branch_name),
                call.on_update_progress(1, 0, 1, ''),
                call.on_update_progress(1, 1, 1, ''),
                call.on_repo_update_finish(repo_name, branch_name),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.update_entry('foo-pkg', repo_name),
                call.update_entry('bar-pkg', repo_name),
                call.update_entry('baz-pkg', repo_name),
                call.update_entry('qux-pkg', repo_name)
            ],
        )

        git_mock.assert_has_calls(
            [
                call(repo_name),
                call().remotes.origin.pull(branch_name)
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_update_with_multiple_repo_and_multiple_packages(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN packages dir is not empty, the mirrors.csv file contains multiple
              repos and it contains only one package.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the correct
              branch, the packages must be added to the packages database and
              the events must be issued to the view properly.

        """
        repo_names = ['foo-repo', 'bar-repo', 'qux-repo']
        repo_urls = [
            'https://github.com/user/{}.git'.format(repo_names[0]),
            'https://github.com/user/{}.git'.format(repo_names[1]),
            'https://github.com/user/{}.git'.format(repo_names[2])
        ]
        branch_name = 'master'

        with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
            mirrors.truncate(0)
            for i in range(len(repo_urls)):
                mirrors.write('{},{}\n'.format(branch_name, repo_urls[i]))

        listdir_mock.return_value = ['foo-pkg']
        isdir_mock.return_value = True

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_repo_update_start(repo_names[0], branch_name),
                call.on_update_progress(1, 0, 1, ''),
                call.on_update_progress(1, 1, 1, ''),
                call.on_repo_update_finish(repo_names[0], branch_name),
                call.on_repo_update_start(repo_names[1], branch_name),
                call.on_update_progress(1, 0, 1, ''),
                call.on_update_progress(1, 1, 1, ''),
                call.on_repo_update_finish(repo_names[1], branch_name),
                call.on_repo_update_start(repo_names[2], branch_name),
                call.on_update_progress(1, 0, 1, ''),
                call.on_update_progress(1, 1, 1, ''),
                call.on_repo_update_finish(repo_names[2], branch_name),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.update_entry('foo-pkg', repo_names[0]),
                call.update_entry('foo-pkg', repo_names[1]),
                call.update_entry('foo-pkg', repo_names[2])
            ]
        )

        git_mock.assert_has_calls(
            [
                call(repo_names[0]),
                call().remotes.origin.pull(branch_name),
                call(repo_names[1]),
                call().remotes.origin.pull(branch_name),
                call(repo_names[2]),
                call().remotes.origin.pull(branch_name)
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_update_with_multiple_repos_and_multiple_packages(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN packages dir is not empty and the mirrors.csv file contains multiple
              repos and each one of them contains multiple packages.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the correct
              branch, the packages must be added into the package database and
              the events must be issued to the view properly.

        """
        repo_names = ['foo-repo', 'bar-repo', 'qux-repo']
        repo_urls = [
            'https://github.com/user/{}.git'.format(repo_names[0]),
            'https://github.com/user/{}.git'.format(repo_names[1]),
            'https://github.com/user/{}.git'.format(repo_names[2])
        ]
        branch_name = 'master'

        with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
            mirrors.truncate(0)
            for i in range(len(repo_urls)):
                mirrors.write('{},{}\n'.format(branch_name, repo_urls[i]))

        listdir_mock.return_value = [
            'foo-pkg',
            'bar-pkg',
            'qux-pkg'
        ]
        isdir_mock.return_value = True

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_repo_update_start(repo_names[0], branch_name),
                call.on_update_progress(1, 0, 1, ''),
                call.on_update_progress(1, 1, 1, ''),
                call.on_repo_update_finish(repo_names[0], branch_name),
                call.on_repo_update_start(repo_names[1], branch_name),
                call.on_update_progress(1, 0, 1, ''),
                call.on_update_progress(1, 1, 1, ''),
                call.on_repo_update_finish(repo_names[1], branch_name),
                call.on_repo_update_start(repo_names[2], branch_name),
                call.on_update_progress(1, 0, 1, ''),
                call.on_update_progress(1, 1, 1, ''),
                call.on_repo_update_finish(repo_names[2], branch_name),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.update_entry('foo-pkg', repo_names[0]),
                call.update_entry('bar-pkg', repo_names[0]),
                call.update_entry('qux-pkg', repo_names[0]),
                call.update_entry('foo-pkg', repo_names[1]),
                call.update_entry('bar-pkg', repo_names[1]),
                call.update_entry('qux-pkg', repo_names[1]),
                call.update_entry('foo-pkg', repo_names[2]),
                call.update_entry('bar-pkg', repo_names[2]),
                call.update_entry('qux-pkg', repo_names[2])
            ]
        )

        git_mock.assert_has_calls(
            [
                call(repo_names[0]),
                call().remotes.origin.pull(branch_name),
                call(repo_names[1]),
                call().remotes.origin.pull(branch_name),
                call(repo_names[2]),
                call().remotes.origin.pull(branch_name)
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_update_with_multiple_repos_with_no_packages(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN packages dir is empty and the mirrors.csv file contains multiple
              repos and each one of them contains multiple packages.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the correct
              branch, no package must be added into the package database and
              the events must be issued to the view properly.

        """
        repo_names = ['foo-repo', 'bar-repo', 'qux-repo']
        repo_urls = [
            'https://github.com/user/{}.git'.format(repo_names[0]),
            'https://github.com/user/{}.git'.format(repo_names[1]),
            'https://github.com/user/{}.git'.format(repo_names[2])
        ]
        branch_name = 'master'

        with open('/etc/gbpm/mirrors.csv', 'w') as mirrors:
            mirrors.truncate(0)
            for i in range(len(repo_urls)):
                mirrors.write('{},{}\n'.format(branch_name, repo_urls[i]))

        listdir_mock.return_value = ['.git']
        isdir_mock.return_value = True

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_repo_update_start(repo_names[0], branch_name),
                call.on_update_progress(1, 0, 1, ''),
                call.on_update_progress(1, 1, 1, ''),
                call.on_repo_update_finish(repo_names[0], branch_name),
                call.on_repo_update_start(repo_names[1], branch_name),
                call.on_update_progress(1, 0, 1, ''),
                call.on_update_progress(1, 1, 1, ''),
                call.on_repo_update_finish(repo_names[1], branch_name),
                call.on_repo_update_start(repo_names[2], branch_name),
                call.on_update_progress(1, 0, 1, ''),
                call.on_update_progress(1, 1, 1, ''),
                call.on_repo_update_finish(repo_names[2], branch_name),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.switch_dir.assert_called_once()
        pkg_mgr_mock.update_entry.assert_not_called()

        git_mock.assert_has_calls(
            [
                call(repo_names[0]),
                call().remotes.origin.pull(branch_name),
                call(repo_names[1]),
                call().remotes.origin.pull(branch_name),
                call(repo_names[2]),
                call().remotes.origin.pull(branch_name)
            ]
        )

if __name__ == "__main__":
    basic_config(level=INFO)
    main()
