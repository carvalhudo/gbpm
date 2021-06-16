from unittest import TestCase, main
from unittest.mock import patch, call, ANY

from commands import ListPkgsCmd
from views import CliListPkgsView

class ListPkgsTest(TestCase):

    """
    Implementation of unit tests for list-pkgs command.

    """

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliListPkgsView')
    def test_list_with_one_not_installed_package(
        self,
        listener_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN the package dir contain only one not installed package.
        WHEN  the user issues an list-pkgs command.
        THEN  the events must be triggered to the view once, according to the
              package found.

        """
        pkg_name = 'foo_pkg'
        master_repo_name = 'fake_repo_1'
        master_user = 'fake_user'
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        pkg_mgr_mock.is_pkg_installed.return_value = False
        isdir_mock.return_value = True
        listdir_mock.side_effect = [
            [master_user],
            [master_repo_name],
            [pkg_name]
        ]

        cmd = ListPkgsCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.is_pkg_installed(pkg_name)
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_pkg_list_start(master_repo_id),
                call.on_pkg_show(pkg_name, False),
                call.on_pkg_list_finish(master_repo_id)
            ]
        )

        isdir_mock.assert_called_once_with(master_user)
        listdir_mock.assert_has_calls(
            [
                call(),
                call(master_user),
                call('{}/src'.format(master_repo_id))
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliListPkgsView')
    def test_list_with_one_installed_package(
        self,
        listener_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN the package dir contain only one installed package.
        WHEN  the user issues an list-pkgs command.
        THEN  the events must be triggered to the view once, according to the
              package found.

        """
        pkg_name = 'foo_pkg'
        master_repo_name = 'fake_repo_1'
        master_user = 'fake_user'
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        pkg_mgr_mock.is_pkg_installed.return_value = True
        isdir_mock.return_value = True
        listdir_mock.side_effect = [
            [master_user],
            [master_repo_name],
            [pkg_name]
        ]

        cmd = ListPkgsCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.is_pkg_installed(pkg_name)
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_pkg_list_start(master_repo_id),
                call.on_pkg_show(pkg_name, True),
                call.on_pkg_list_finish(master_repo_id)
            ]
        )

        isdir_mock.assert_called_once_with(master_user)
        listdir_mock.assert_has_calls(
            [
                call(),
                call(master_user),
                call('{}/src'.format(master_repo_id))
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliListPkgsView')
    def test_list_with_multiple_not_installed_packages(
        self,
        listener_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN the package dir contain multiple not installed packages.
        WHEN  the user issues an list-pkgs command.
        THEN  the events must be triggered to the view multiple times, according
              to the number of packages found.

        """
        pkg_names = ['foo_pkg', 'bar_pkg', 'baz_pkg']
        master_repo_name = 'fake_repo_1'
        master_user = 'fake_user'
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        pkg_mgr_mock.is_pkg_installed.return_value = False
        isdir_mock.return_value = True
        listdir_mock.side_effect = [
            [master_user],
            [master_repo_name],
            pkg_names
        ]

        cmd = ListPkgsCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.is_pkg_installed(pkg_names[0]),
                call.is_pkg_installed(pkg_names[1]),
                call.is_pkg_installed(pkg_names[2])
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_pkg_list_start(master_repo_id),
                call.on_pkg_show(pkg_names[0], False),
                call.on_pkg_show(pkg_names[1], False),
                call.on_pkg_show(pkg_names[2], False),
                call.on_pkg_list_finish(master_repo_id)
            ]
        )

        isdir_mock.assert_called_once_with(master_user)
        listdir_mock.assert_has_calls(
            [
                call(),
                call(master_user),
                call('{}/src'.format(master_repo_id))
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliListPkgsView')
    def test_list_with_multiple_installed_packages(
        self,
        listener_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN the package dir contain multiple installed packages.
        WHEN  the user issues an list-pkgs command.
        THEN  the events must be triggered to the view multiple times, according
              to the number of packages found.

        """
        pkg_names = ['foo_pkg', 'bar_pkg', 'baz_pkg']
        master_repo_name = 'fake_repo_1'
        master_user = 'fake_user'
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        pkg_mgr_mock.is_pkg_installed.return_value = True
        isdir_mock.return_value = True
        listdir_mock.side_effect = [
            [master_user],
            [master_repo_name],
            pkg_names
        ]

        cmd = ListPkgsCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
                call.is_pkg_installed(pkg_names[0]),
                call.is_pkg_installed(pkg_names[1]),
                call.is_pkg_installed(pkg_names[2])
            ]
        )

        listener_mock.assert_has_calls(
            [
                call.on_pkg_list_start(master_repo_id),
                call.on_pkg_show(pkg_names[0], True),
                call.on_pkg_show(pkg_names[1], True),
                call.on_pkg_show(pkg_names[2], True),
                call.on_pkg_list_finish(master_repo_id)
            ]
        )

        isdir_mock.assert_called_once_with(master_user)
        listdir_mock.assert_has_calls(
            [
                call(),
                call(master_user),
                call('{}/src'.format(master_repo_id))
            ]
        )

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('views.CliListPkgsView')
    def test_list_with_no_packages(
        self,
        listener_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock):
        """
        GIVEN the package dir is empty.
        WHEN  the user issues an list-pkgs command.
        THEN  no on_pkg_show events must be triggered to the view multiple.

        """
        master_repo_name = 'fake_repo_1'
        master_user = 'fake_user'
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        pkg_mgr_mock.is_pkg_installed.return_value = False
        isdir_mock.return_value = True
        listdir_mock.side_effect = [
            [master_user],
            [master_repo_name],
            []
        ]

        cmd = ListPkgsCmd(pkg_mgr_mock)
        cmd.execute(listener_mock)

        pkg_mgr_mock.assert_has_calls(
            [
                call.switch_dir(),
            ]
        )

        pkg_mgr_mock.is_pkg_installed.assert_not_called()

        listener_mock.assert_has_calls(
            [
                call.on_pkg_list_start(master_repo_id),
                call.on_pkg_list_finish(master_repo_id)
            ]
        )

        listener_mock.on_pkg_show.assert_not_called()

        isdir_mock.assert_called_once_with(master_user)
        listdir_mock.assert_has_calls(
            [
                call(),
                call(master_user),
                call('{}/src'.format(master_repo_id))
            ]
        )
        pass

    # TODO: multiple users and multiple repos

if __name__ == "__main__":
    main()
