from unittest import TestCase, main
from unittest.mock import patch, call

import git

from commands import UpdateCmd
from errors import error_map

class UpdateTest(TestCase):

    """
    Implementation of unit tests for update command.

    """

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('commands.UpdateCmd.InitializeRepoCmd')
    @patch('os.path.isdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliUpdateView')
    def test_initialize_single_repo(
        self,
        listener_mock,
        pkg_mgr_mock,
        isdir_mock,
        cmd_mock,
        mirrors_mock):
        """
        GIVEN the package dir is empty and the mirrors file contains only one
              repo.
        WHEN  the user issues an update command.
        THEN  the command 'InitializeRepo' must be executed and the events
              must be issued to the view properly.

        """
        master_repo_name = 'fake_repo_1'
        master_branch_name = 'master'
        master_user = 'fake_user'
        repo_url = 'https://github.com/{}/{}.git'.format(
            master_user,
            master_repo_name
        )
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        isdir_mock.return_value = False
        mirrors_mock.return_value = [
            '{},{}'.format(master_branch_name, repo_url)
        ]

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        mirrors_mock.assert_has_calls(
            [
                call()
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_master_repo_update_start(
                    master_repo_id,
                    master_branch_name
                ),
                call.on_master_repo_update_finish(
                    master_repo_id,
                    master_branch_name
                ),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir()
            ]
        )

        cmd_mock.assert_has_calls(
            [
                call(pkg_mgr_mock, master_repo_id, master_branch_name, repo_url),
                call(
                    pkg_mgr_mock,
                    master_repo_id,
                    master_branch_name,
                    repo_url
                ).execute(listener_mock)
            ]
        )

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('commands.UpdateCmd.InitializeRepoCmd')
    @patch('os.path.isdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliUpdateView')
    def test_initialize_multiple_repos(
        self,
        listener_mock,
        pkg_mgr_mock,
        isdir_mock,
        cmd_mock,
        mirrors_mock):
        """
        GIVEN the package dir is empty and the mirrors file contains multiple
              repos.
        WHEN  the user issues an update command.
        THEN  the command 'InitializeRepo' must be executed 'n' times and the
              events must be issued to the view properly.

        """
        master_repo_names = ['fake_repo_1', 'fake_repo_2', 'fake_repo_3']
        master_branch_name = 'master'
        master_user = 'fake_user'
        repo_urls = [
            'https://github.com/{}/{}.git'.format(master_user, master_repo_names[0]),
            'https://github.com/{}/{}.git'.format(master_user, master_repo_names[1]),
            'https://github.com/{}/{}.git'.format(master_user, master_repo_names[2])
        ]
        master_repo_ids = [
            '{}/{}'.format(master_user, master_repo_names[0]),
            '{}/{}'.format(master_user, master_repo_names[1]),
            '{}/{}'.format(master_user, master_repo_names[2])
        ]

        isdir_mock.return_value = False
        mirrors_mock.return_value = [
            '{},{}'.format(master_branch_name, repo_urls[0]),
            '{},{}'.format(master_branch_name, repo_urls[1]),
            '{},{}'.format(master_branch_name, repo_urls[2])
        ]

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        mirrors_mock.assert_has_calls(
            [
                call()
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_master_repo_update_start(
                    master_repo_ids[0],
                    master_branch_name
                ),
                call.on_master_repo_update_finish(
                    master_repo_ids[0],
                    master_branch_name
                ),
                call.on_master_repo_update_start(
                    master_repo_ids[1],
                    master_branch_name
                ),
                call.on_master_repo_update_finish(
                    master_repo_ids[1],
                    master_branch_name
                ),
                call.on_master_repo_update_start(
                    master_repo_ids[2],
                    master_branch_name
                ),
                call.on_master_repo_update_finish(
                    master_repo_ids[2],
                    master_branch_name
                ),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir()
            ]
        )

        cmd_mock.assert_has_calls(
            [
                call(pkg_mgr_mock, master_repo_ids[0], master_branch_name, repo_urls[0]),
                call(
                    pkg_mgr_mock,
                    master_repo_ids[0],
                    master_branch_name,
                    repo_urls[0]
                ).execute(listener_mock),
                call(pkg_mgr_mock, master_repo_ids[1], master_branch_name, repo_urls[1]),
                call(
                    pkg_mgr_mock,
                    master_repo_ids[1],
                    master_branch_name,
                    repo_urls[1]
                ).execute(listener_mock),
                call(pkg_mgr_mock, master_repo_ids[2], master_branch_name, repo_urls[2]),
                call(
                    pkg_mgr_mock,
                    master_repo_ids[2],
                    master_branch_name,
                    repo_urls[2]
                ).execute(listener_mock)
            ]
        )

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('commands.UpdateCmd.UpdateRepoCmd')
    @patch('os.path.isdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliUpdateView')
    def test_update_single_repo(
        self,
        listener_mock,
        pkg_mgr_mock,
        isdir_mock,
        cmd_mock,
        mirrors_mock):
        """
        GIVEN the package dir is not empty and the mirrors file contains only
              one repo.
        WHEN  the user issues an update command.
        THEN  the command 'UpdateRepo' must be executed once and the events
              must be issued to the view properly.

        """
        master_repo_name = 'fake_repo_1'
        master_branch_name = 'master'
        master_user = 'fake_user'
        repo_url = 'https://github.com/{}/{}.git'.format(
            master_user,
            master_repo_name
        )
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        isdir_mock.return_value = True
        mirrors_mock.return_value = [
            '{},{}'.format(master_branch_name, repo_url)
        ]

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        mirrors_mock.assert_has_calls(
            [
                call()
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_master_repo_update_start(
                    master_repo_id,
                    master_branch_name
                ),
                call.on_master_repo_update_finish(
                    master_repo_id,
                    master_branch_name
                ),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir()
            ]
        )

        cmd_mock.assert_has_calls(
            [
                call(pkg_mgr_mock, master_repo_id, master_branch_name),
                call(
                    pkg_mgr_mock,
                    master_repo_id,
                    master_branch_name
                ).execute(listener_mock)
            ]
        )

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('commands.UpdateCmd.UpdateRepoCmd')
    @patch('os.path.isdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliUpdateView')
    def test_update_multiple_repos(
        self,
        listener_mock,
        pkg_mgr_mock,
        isdir_mock,
        cmd_mock,
        mirrors_mock):
        """
        GIVEN the package dir is not empty and the mirrors file contains
              multiple repos.
        WHEN  the user issues an update command.
        THEN  the command 'UpdateRepo' must be executed 'n' times and the
              events must be issued to the view properly.

        """
        master_repo_names = ['fake_repo_1', 'fake_repo_2', 'fake_repo_3']
        master_branch_name = 'master'
        master_user = 'fake_user'
        repo_urls = [
            'https://github.com/{}/{}.git'.format(master_user, master_repo_names[0]),
            'https://github.com/{}/{}.git'.format(master_user, master_repo_names[1]),
            'https://github.com/{}/{}.git'.format(master_user, master_repo_names[2])
        ]
        master_repo_ids = [
            '{}/{}'.format(master_user, master_repo_names[0]),
            '{}/{}'.format(master_user, master_repo_names[1]),
            '{}/{}'.format(master_user, master_repo_names[2])
        ]

        isdir_mock.return_value = True
        mirrors_mock.return_value = [
            '{},{}'.format(master_branch_name, repo_urls[0]),
            '{},{}'.format(master_branch_name, repo_urls[1]),
            '{},{}'.format(master_branch_name, repo_urls[2])
        ]

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        mirrors_mock.assert_has_calls(
            [
                call()
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_master_repo_update_start(
                    master_repo_ids[0],
                    master_branch_name
                ),
                call.on_master_repo_update_finish(
                    master_repo_ids[0],
                    master_branch_name
                ),
                call.on_master_repo_update_start(
                    master_repo_ids[1],
                    master_branch_name
                ),
                call.on_master_repo_update_finish(
                    master_repo_ids[1],
                    master_branch_name
                ),
                call.on_master_repo_update_start(
                    master_repo_ids[2],
                    master_branch_name
                ),
                call.on_master_repo_update_finish(
                    master_repo_ids[2],
                    master_branch_name
                ),
                call.on_update_finish()
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir()
            ]
        )

        cmd_mock.assert_has_calls(
            [
                call(pkg_mgr_mock, master_repo_ids[0], master_branch_name),
                call(
                    pkg_mgr_mock,
                    master_repo_ids[0],
                    master_branch_name
                ).execute(listener_mock),
                call(pkg_mgr_mock, master_repo_ids[1], master_branch_name),
                call(
                    pkg_mgr_mock,
                    master_repo_ids[1],
                    master_branch_name
                ).execute(listener_mock),
                call(pkg_mgr_mock, master_repo_ids[2], master_branch_name),
                call(
                    pkg_mgr_mock,
                    master_repo_ids[2],
                    master_branch_name
                ).execute(listener_mock)
            ]
        )

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('commands.UpdateCmd.InitializeRepoCmd')
    @patch('os.path.isdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliUpdateView')
    def test_initialize_repo_with_clone_error(
        self,
        listener_mock,
        pkg_mgr_mock,
        isdir_mock,
        cmd_mock,
        mirrors_mock):
        """
        GIVEN the package dir is empty and the mirrors file contains only one
              repo.
        WHEN  the user issues an update command and an error during the clone of
              the repository occurs.
        THEN  the proper event 'on_error' must be triggered to the view with the
              suitable error message.

        """
        master_repo_name = 'fake_repo_1'
        master_branch_name = 'master'
        master_user = 'fake_user'
        repo_url = 'https://github.com/{}/{}.git'.format(
            master_user,
            master_repo_name
        )
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        isdir_mock.return_value = False
        mirrors_mock.return_value = [
            '{},{}'.format(master_branch_name, repo_url)
        ]
        cmd_mock().execute.side_effect = git.GitCommandError('git clone', '')

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        mirrors_mock.assert_has_calls(
            [
                call()
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_master_repo_update_start(
                    master_repo_id,
                    master_branch_name
                ),
                call.on_update_progress(1, 1, 1, ''),
                call.on_error('{} {}'.format(error_map['clone'], master_repo_id)),
                call.on_update_finish(),
            ]
        )

        listener_mock.on_master_update_finish.assert_not_called()

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir()
            ]
        )

        cmd_mock.assert_has_calls(
            [
                call(pkg_mgr_mock, master_repo_id, master_branch_name, repo_url),
                call(
                    pkg_mgr_mock,
                    master_repo_id,
                    master_branch_name,
                    repo_url
                ).execute(listener_mock)
            ]
        )

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('commands.UpdateCmd.InitializeRepoCmd')
    @patch('os.path.isdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliUpdateView')
    def test_initialize_repo_with_fetch_error(
        self,
        listener_mock,
        pkg_mgr_mock,
        isdir_mock,
        cmd_mock,
        mirrors_mock):
        """
        GIVEN the package dir is empty and the mirrors file contains only one
              repo.
        WHEN  the user issues an update command and an error during the fetch of
              the repository occurs.
        THEN  the proper event 'on_error' must be triggered to the view with the
              suitable error message.

        """
        master_repo_name = 'fake_repo_1'
        master_branch_name = 'master'
        master_user = 'fake_user'
        repo_url = 'https://github.com/{}/{}.git'.format(
            master_user,
            master_repo_name
        )
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        isdir_mock.return_value = False
        mirrors_mock.return_value = [
            '{},{}'.format(master_branch_name, repo_url)
        ]
        cmd_mock().execute.side_effect = git.GitCommandError('git fetch', '')

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        mirrors_mock.assert_has_calls(
            [
                call()
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_master_repo_update_start(
                    master_repo_id,
                    master_branch_name
                ),
                call.on_update_progress(1, 1, 1, ''),
                call.on_error('{} {}'.format(error_map['fetch'], master_repo_id)),
                call.on_update_finish(),
            ]
        )

        listener_mock.on_master_update_finish.assert_not_called()

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir()
            ]
        )

        cmd_mock.assert_has_calls(
            [
                call(pkg_mgr_mock, master_repo_id, master_branch_name, repo_url),
                call(
                    pkg_mgr_mock,
                    master_repo_id,
                    master_branch_name,
                    repo_url
                ).execute(listener_mock)
            ]
        )

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('commands.UpdateCmd.InitializeRepoCmd')
    @patch('os.path.isdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliUpdateView')
    def test_initialize_repo_with_pull_error(
        self,
        listener_mock,
        pkg_mgr_mock,
        isdir_mock,
        cmd_mock,
        mirrors_mock):
        """
        GIVEN the package dir is empty and the mirrors file contains only one
              repo.
        WHEN  the user issues an update command and an error during the pull of
              the repository occurs.
        THEN  the proper event 'on_error' must be triggered to the view with the
              suitable error message.

        """
        master_repo_name = 'fake_repo_1'
        master_branch_name = 'master'
        master_user = 'fake_user'
        repo_url = 'https://github.com/{}/{}.git'.format(
            master_user,
            master_repo_name
        )
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        isdir_mock.return_value = False
        mirrors_mock.return_value = [
            '{},{}'.format(master_branch_name, repo_url)
        ]
        cmd_mock().execute.side_effect = git.GitCommandError('git pull', '')

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        mirrors_mock.assert_has_calls(
            [
                call()
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_master_repo_update_start(
                    master_repo_id,
                    master_branch_name
                ),
                call.on_update_progress(1, 1, 1, ''),
                call.on_error('{} {}'.format(error_map['pull'], master_repo_id)),
                call.on_update_finish(),
            ]
        )

        listener_mock.on_master_update_finish.assert_not_called()

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir()
            ]
        )

        cmd_mock.assert_has_calls(
            [
                call(pkg_mgr_mock, master_repo_id, master_branch_name, repo_url),
                call(
                    pkg_mgr_mock,
                    master_repo_id,
                    master_branch_name,
                    repo_url
                ).execute(listener_mock)
            ]
        )

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('commands.UpdateCmd.InitializeRepoCmd')
    @patch('os.path.isdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliUpdateView')
    def test_initialize_repo_with_unknown_error(
        self,
        listener_mock,
        pkg_mgr_mock,
        isdir_mock,
        cmd_mock,
        mirrors_mock):
        """
        GIVEN the package dir is empty and the mirrors file contains only one
              repo.
        WHEN  the user issues an update command and an non-mapped error occurs.
        THEN  the proper event 'on_error' must be triggered to the view with the
              suitable error message.

        """
        master_repo_name = 'fake_repo_1'
        master_branch_name = 'master'
        master_user = 'fake_user'
        repo_url = 'https://github.com/{}/{}.git'.format(
            master_user,
            master_repo_name
        )
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        isdir_mock.return_value = False
        mirrors_mock.return_value = [
            '{},{}'.format(master_branch_name, repo_url)
        ]
        cmd_mock().execute.side_effect = ValueError('foo')

        cmd = UpdateCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        mirrors_mock.assert_has_calls(
            [
                call()
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_update_start(),
                call.on_master_repo_update_start(
                    master_repo_id,
                    master_branch_name
                ),
                call.on_update_progress(1, 1, 1, ''),
                call.on_error(error_map['unknown']),
                call.on_update_finish(),
            ]
        )

        listener_mock.on_master_update_finish.assert_not_called()

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir()
            ]
        )

        cmd_mock.assert_has_calls(
            [
                call(pkg_mgr_mock, master_repo_id, master_branch_name, repo_url),
                call(
                    pkg_mgr_mock,
                    master_repo_id,
                    master_branch_name,
                    repo_url
                ).execute(listener_mock)
            ]
        )

if __name__ == "__main__":
    main()
