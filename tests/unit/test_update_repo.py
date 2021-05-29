from unittest import TestCase, main
from unittest.mock import patch, call, ANY

from errors import error_map
from os import chdir
import git

from commands import UpdateCmd

class UpdateRepoTest(TestCase):

    """
    Implementation of unit tests for update repo command.

    """
    def setUpClass():
        chdir('resources/')

    def tearDownClass():
        chdir('../')

    #@patch('os.path.isdir')
    #@patch('os.listdir')
    #@patch('package_database_mgr.PackageDatabaseMgr')
    #@patch('git.Repo')
    #@patch('views.CliUpdateView')
    #def test_update_with_single_repo_and_single_package(
    #    self,
    #    listener_mock,
    #    git_mock,
    #    pkg_mgr_mock,
    #    listdir_mock,
    #    isdir_mock):
    #    """
    #    GIVEN packages dir is not empty, the mirrors.csv file contains
    #          only one repo and it contains only one package.
    #    WHEN  the user issues an update command.
    #    THEN  the repository must be pulled from origin, the package must
    #          be added into the package database and the events must be
    #          issued to the view properly.

    #    """
    #    pkg_name = 'foo_pkg'
    #    pkg_branch = 'foo_branch'
    #    master_repo_name = 'fake_repo_1'
    #    master_branch_name = 'master'
    #    master_user = 'fake_user'
    #    repo_url = 'https://github.com/{}/{}.git'.format(
    #        master_user,
    #        master_repo_name
    #    )
    #    master_repo_id = '{}/{}'.format(master_user, master_repo_name)

    #    with open('/etc/gur/mirrors.csv', 'w') as mirrors:
    #        mirrors.write('{},{}'.format(master_branch_name, repo_url))

    #    listdir_mock.return_value = [pkg_name]
    #    isdir_mock.return_value = True

    #    cmd = UpdateCmd(pkg_mgr_mock)
    #    cmd.execute(listener_mock)

    #    listener_mock.assert_has_calls(
    #        [
    #            call.on_update_start(),

    #            call.on_repo_update_start(master_repo_id, master_branch_name),
    #            call.on_update_progress(1, 0, 1, 'Pulling master repo ...'),
    #            call.on_update_progress(1, 1, 1, 'Pulling master repo ...'),
    #            call.on_pkg_update_start(pkg_name, pkg_branch),
    #            call.on_pkg_update_finish(pkg_name, pkg_branch),
    #            call.on_repo_update_finish(master_repo_id, master_branch_name),

    #            call.on_update_finish()
    #        ]
    #    )

    #    pkg_mgr_mock.assert_has_calls(
    #        [
    #            call.switch_dir(),
    #            call.update_entry(pkg_name, ANY) # TODO
    #        ]
    #    )

    #    git_mock.assert_has_calls(
    #        [
    #            call(master_repo_id),
    #            call().remotes.origin.pull(master_branch_name),
    #            call('{}/src/{}/.repo'.format(master_repo_id, pkg_name)),
    #            call().remotes.origin.fetch(progress=ANY), # TODO
    #            call().rev_parse('origin/{}'.format(pkg_branch))
    #        ]
    #    )

    #@patch('os.path.isdir')
    #@patch('os.listdir')
    #@patch('package_database_mgr.PackageDatabaseMgr')
    #@patch('git.Repo')
    #@patch('views.CliUpdateView')
    #def test_update_with_single_repo_and_multiple_packages(
    #    self,
    #    listener_mock,
    #    git_mock,
    #    pkg_mgr_mock,
    #    listdir_mock,
    #    isdir_mock):
    #    """
    #    GIVEN packages dir is not empty, the mirrors.csv file contains only
    #          one repo and it contains multiple packages.
    #    WHEN  the user issues an update command.
    #    THEN  the repository must be cloned into the packages dir in the correct
    #          branch, the packages must be added into the package database and
    #          the events must be issued to the view properly.

    #    """
    #    pkg_names = ['foo_pkg', 'bar_pkg', 'baz_pkg', 'qux_pkg']
    #    pkg_branches = ['foo_branch', 'bar_branch', 'baz_branch', 'qux_branch']
    #    master_repo_name = 'fake_repo_1'
    #    master_branch_name = 'master'
    #    master_user = 'fake_user'
    #    repo_url = 'https://github.com/{}/{}.git'.format(
    #        master_user,
    #        master_repo_name
    #    )
    #    master_repo_id = '{}/{}'.format(master_user, master_repo_name)

    #    with open('/etc/gur/mirrors.csv', 'w') as mirrors:
    #        mirrors.truncate(0)
    #        mirrors.write('{},{}'.format(master_branch_name, repo_url))

    #    listdir_mock.return_value = pkg_names
    #    isdir_mock.return_value = True

    #    cmd = UpdateCmd(pkg_mgr_mock)
    #    cmd.execute(listener_mock)

    #    listener_mock.assert_has_calls(
    #        [
    #            call.on_update_start(),

    #            call.on_repo_update_start(master_repo_id, master_branch_name),
    #            call.on_update_progress(1, 0, 1, 'Pulling master repo ...'),
    #            call.on_update_progress(1, 1, 1, 'Pulling master repo ...'),
    #            call.on_pkg_update_start(pkg_names[0], pkg_branches[0]),
    #            call.on_pkg_update_finish(pkg_names[0], pkg_branches[0]),
    #            call.on_pkg_update_start(pkg_names[1], pkg_branches[1]),
    #            call.on_pkg_update_finish(pkg_names[1], pkg_branches[1]),
    #            call.on_pkg_update_start(pkg_names[2], pkg_branches[2]),
    #            call.on_pkg_update_finish(pkg_names[2], pkg_branches[2]),
    #            call.on_pkg_update_start(pkg_names[3], pkg_branches[3]),
    #            call.on_pkg_update_finish(pkg_names[3], pkg_branches[3]),
    #            call.on_repo_update_finish(master_repo_id, master_branch_name),

    #            call.on_update_finish()
    #        ]
    #    )

    #    pkg_mgr_mock.assert_has_calls(
    #        [
    #            call.switch_dir(),
    #            call.update_entry(pkg_names[0], ANY),
    #            call.update_entry(pkg_names[1], ANY),
    #            call.update_entry(pkg_names[2], ANY),
    #            call.update_entry(pkg_names[3], ANY)
    #        ],
    #    )

    #    git_mock.assert_has_calls(
    #        [
    #            call(master_repo_id),
    #            call().remotes.origin.pull(master_branch_name),

    #            call('{}/src/{}/.repo'.format(master_repo_id, pkg_names[0])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[0])),

    #            call('{}/src/{}/.repo'.format(master_repo_id, pkg_names[1])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[1])),

    #            call('{}/src/{}/.repo'.format(master_repo_id, pkg_names[2])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[2])),

    #            call('{}/src/{}/.repo'.format(master_repo_id, pkg_names[3])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[3]))
    #        ]
    #    )

    #@patch('os.path.isdir')
    #@patch('os.listdir')
    #@patch('package_database_mgr.PackageDatabaseMgr')
    #@patch('git.Repo')
    #@patch('views.CliUpdateView')
    #def test_update_with_multiple_repos_and_single_package(
    #    self,
    #    listener_mock,
    #    git_mock,
    #    pkg_mgr_mock,
    #    listdir_mock,
    #    isdir_mock):
    #    """
    #    GIVEN packages dir is not empty, the mirrors.csv file contains multiple
    #          repos and it contains only one package.
    #    WHEN  the user issues an update command.
    #    THEN  the repository must be cloned into the packages dir in the correct
    #          branch, the packages must be added to the packages database and
    #          the events must be issued to the view properly.

    #    """
    #    pkg_name = 'foo_pkg'
    #    pkg_branch = 'foo_branch'
    #    master_repo_names = ['fake_repo_1', 'fake_repo_2', 'fake_repo_3']
    #    master_branch_name = 'master'
    #    master_user = 'fake_user'
    #    repo_urls = [
    #        'https://github.com/{}/{}.git'.format(master_user, master_repo_names[0]),
    #        'https://github.com/{}/{}.git'.format(master_user, master_repo_names[1]),
    #        'https://github.com/{}/{}.git'.format(master_user, master_repo_names[2])
    #    ]
    #    master_repo_ids = [
    #        '{}/{}'.format(master_user, master_repo_names[0]),
    #        '{}/{}'.format(master_user, master_repo_names[1]),
    #        '{}/{}'.format(master_user, master_repo_names[2])
    #    ]

    #    with open('/etc/gur/mirrors.csv', 'w') as mirrors:
    #        mirrors.truncate(0)
    #        for i in range(len(repo_urls)):
    #            mirrors.write('{},{}\n'.format(master_branch_name, repo_urls[i]))

    #    listdir_mock.return_value = [pkg_name]
    #    isdir_mock.return_value = True

    #    cmd = UpdateCmd(pkg_mgr_mock)
    #    cmd.execute(listener_mock)

    #    listener_mock.assert_has_calls(
    #        [
    #            call.on_update_start(),

    #            call.on_repo_update_start(master_repo_ids[0], master_branch_name),
    #            call.on_update_progress(1, 0, 1, 'Pulling master repo ...'),
    #            call.on_update_progress(1, 1, 1, 'Pulling master repo ...'),
    #            call.on_pkg_update_start(pkg_name, pkg_branch),
    #            call.on_pkg_update_finish(pkg_name, pkg_branch),
    #            call.on_repo_update_finish(master_repo_ids[0], master_branch_name),

    #            call.on_repo_update_start(master_repo_ids[1], master_branch_name),
    #            call.on_update_progress(1, 0, 1, 'Pulling master repo ...'),
    #            call.on_update_progress(1, 1, 1, 'Pulling master repo ...'),
    #            call.on_pkg_update_start(pkg_name, pkg_branch),
    #            call.on_pkg_update_finish(pkg_name, pkg_branch),
    #            call.on_repo_update_finish(master_repo_ids[1], master_branch_name),

    #            call.on_repo_update_start(master_repo_ids[2], master_branch_name),
    #            call.on_update_progress(1, 0, 1, 'Pulling master repo ...'),
    #            call.on_update_progress(1, 1, 1, 'Pulling master repo ...'),
    #            call.on_pkg_update_start(pkg_name, pkg_branch),
    #            call.on_pkg_update_finish(pkg_name, pkg_branch),
    #            call.on_repo_update_finish(master_repo_ids[2], master_branch_name),

    #            call.on_update_finish()
    #        ]
    #    )

    #    pkg_mgr_mock.assert_has_calls(
    #        [
    #            call.switch_dir(),
    #            call.update_entry(pkg_name, ANY),
    #            call.update_entry(pkg_name, ANY),
    #            call.update_entry(pkg_name, ANY)
    #        ]
    #    )

    #    git_mock.assert_has_calls(
    #        [
    #            call(master_repo_ids[0]),
    #            call().remotes.origin.pull(master_branch_name),

    #            call('{}/src/{}/.repo'.format(master_repo_ids[0], pkg_name)),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branch)),

    #            call(master_repo_ids[1]),
    #            call().remotes.origin.pull(master_branch_name),

    #            call('{}/src/{}/.repo'.format(master_repo_ids[1], pkg_name)),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branch)),

    #            call(master_repo_ids[2]),
    #            call().remotes.origin.pull(master_branch_name),

    #            call('{}/src/{}/.repo'.format(master_repo_ids[2], pkg_name)),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branch)),
    #        ]
    #    )

    #@patch('os.path.isdir')
    #@patch('os.listdir')
    #@patch('package_database_mgr.PackageDatabaseMgr')
    #@patch('git.Repo')
    #@patch('views.CliUpdateView')
    #def test_update_with_multiple_repos_and_multiple_packages(
    #    self,
    #    listener_mock,
    #    git_mock,
    #    pkg_mgr_mock,
    #    listdir_mock,
    #    isdir_mock):
    #    """
    #    GIVEN packages dir is not empty and the mirrors.csv file contains multiple
    #          repos and each one of them contains multiple packages.
    #    WHEN  the user issues an update command.
    #    THEN  the repository must be cloned into the packages dir in the correct
    #          branch, the packages must be added into the package database and
    #          the events must be issued to the view properly.

    #    """
    #    pkg_names = ['foo_pkg', 'bar_pkg', 'qux_pkg']
    #    pkg_branches = ['foo_branch', 'bar_branch', 'qux_branch']
    #    master_repo_names = ['fake_repo_1', 'fake_repo_2', 'fake_repo_3']
    #    master_branch_name = 'master'
    #    master_user = 'fake_user'
    #    repo_urls = [
    #        'https://github.com/{}/{}.git'.format(master_user, master_repo_names[0]),
    #        'https://github.com/{}/{}.git'.format(master_user, master_repo_names[1]),
    #        'https://github.com/{}/{}.git'.format(master_user, master_repo_names[2])
    #    ]
    #    master_repo_ids = [
    #        '{}/{}'.format(master_user, master_repo_names[0]),
    #        '{}/{}'.format(master_user, master_repo_names[1]),
    #        '{}/{}'.format(master_user, master_repo_names[2])
    #    ]

    #    with open('/etc/gur/mirrors.csv', 'w') as mirrors:
    #        mirrors.truncate(0)
    #        for i in range(len(repo_urls)):
    #            mirrors.write('{},{}\n'.format(master_branch_name, repo_urls[i]))

    #    listdir_mock.return_value = pkg_names
    #    isdir_mock.return_value = True

    #    cmd = UpdateCmd(pkg_mgr_mock)
    #    cmd.execute(listener_mock)

    #    listener_mock.assert_has_calls(
    #        [
    #            call.on_update_start(),

    #            call.on_repo_update_start(master_repo_ids[0], master_branch_name),
    #            call.on_update_progress(1, 0, 1, 'Pulling master repo ...'),
    #            call.on_update_progress(1, 1, 1, 'Pulling master repo ...'),
    #            call.on_pkg_update_start(pkg_names[0], pkg_branches[0]),
    #            call.on_pkg_update_finish(pkg_names[0], pkg_branches[0]),
    #            call.on_pkg_update_start(pkg_names[1], pkg_branches[1]),
    #            call.on_pkg_update_finish(pkg_names[1], pkg_branches[1]),
    #            call.on_pkg_update_start(pkg_names[2], pkg_branches[2]),
    #            call.on_pkg_update_finish(pkg_names[2], pkg_branches[2]),
    #            call.on_repo_update_finish(master_repo_ids[0], master_branch_name),

    #            call.on_repo_update_start(master_repo_ids[1], master_branch_name),
    #            call.on_update_progress(1, 0, 1, 'Pulling master repo ...'),
    #            call.on_update_progress(1, 1, 1, 'Pulling master repo ...'),
    #            call.on_pkg_update_start(pkg_names[0], pkg_branches[0]),
    #            call.on_pkg_update_finish(pkg_names[0], pkg_branches[0]),
    #            call.on_pkg_update_start(pkg_names[1], pkg_branches[1]),
    #            call.on_pkg_update_finish(pkg_names[1], pkg_branches[1]),
    #            call.on_pkg_update_start(pkg_names[2], pkg_branches[2]),
    #            call.on_pkg_update_finish(pkg_names[2], pkg_branches[2]),
    #            call.on_repo_update_finish(master_repo_ids[1], master_branch_name),

    #            call.on_repo_update_start(master_repo_ids[2], master_branch_name),
    #            call.on_update_progress(1, 0, 1, 'Pulling master repo ...'),
    #            call.on_update_progress(1, 1, 1, 'Pulling master repo ...'),
    #            call.on_pkg_update_start(pkg_names[0], pkg_branches[0]),
    #            call.on_pkg_update_finish(pkg_names[0], pkg_branches[0]),
    #            call.on_pkg_update_start(pkg_names[1], pkg_branches[1]),
    #            call.on_pkg_update_finish(pkg_names[1], pkg_branches[1]),
    #            call.on_pkg_update_start(pkg_names[2], pkg_branches[2]),
    #            call.on_pkg_update_finish(pkg_names[2], pkg_branches[2]),
    #            call.on_repo_update_finish(master_repo_ids[2], master_branch_name),

    #            call.on_update_finish()
    #        ]
    #    )

    #    pkg_mgr_mock.assert_has_calls(
    #        [
    #            call.switch_dir(),
    #            call.update_entry(pkg_names[0], ANY),
    #            call.update_entry(pkg_names[1], ANY),
    #            call.update_entry(pkg_names[2], ANY),
    #            call.update_entry(pkg_names[0], ANY),
    #            call.update_entry(pkg_names[1], ANY),
    #            call.update_entry(pkg_names[2], ANY),
    #            call.update_entry(pkg_names[0], ANY),
    #            call.update_entry(pkg_names[1], ANY),
    #            call.update_entry(pkg_names[2], ANY)
    #        ]
    #    )

    #    git_mock.assert_has_calls(
    #        [
    #            call(master_repo_ids[0]),
    #            call().remotes.origin.pull(master_branch_name),
    #            call('{}/src/{}/.repo'.format(master_repo_ids[0], pkg_names[0])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[0])),
    #            call('{}/src/{}/.repo'.format(master_repo_ids[0], pkg_names[1])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[1])),
    #            call('{}/src/{}/.repo'.format(master_repo_ids[0], pkg_names[2])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[2])),

    #            call(master_repo_ids[1]),
    #            call().remotes.origin.pull(master_branch_name),
    #            call('{}/src/{}/.repo'.format(master_repo_ids[1], pkg_names[0])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[0])),
    #            call('{}/src/{}/.repo'.format(master_repo_ids[1], pkg_names[1])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[1])),
    #            call('{}/src/{}/.repo'.format(master_repo_ids[1], pkg_names[2])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[2])),

    #            call(master_repo_ids[2]),
    #            call().remotes.origin.pull(master_branch_name),
    #            call('{}/src/{}/.repo'.format(master_repo_ids[2], pkg_names[0])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[0])),
    #            call('{}/src/{}/.repo'.format(master_repo_ids[2], pkg_names[1])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[1])),
    #            call('{}/src/{}/.repo'.format(master_repo_ids[2], pkg_names[2])),
    #            call().remotes.origin.fetch(progress=ANY),
    #            call().rev_parse('origin/{}'.format(pkg_branches[2]))
    #        ]
    #    )

    #@patch('os.path.isdir')
    #@patch('os.listdir')
    #@patch('package_database_mgr.PackageDatabaseMgr')
    #@patch('git.Repo')
    #@patch('views.CliUpdateView')
    #def test_update_with_multiple_repos_with_no_packages(
    #    self,
    #    listener_mock,
    #    git_mock,
    #    pkg_mgr_mock,
    #    listdir_mock,
    #    isdir_mock):
    #    """
    #    GIVEN packages dir is empty and the mirrors.csv file contains multiple
    #          repos and each one of them contains multiple packages.
    #    WHEN  the user issues an update command.
    #    THEN  the repository must be cloned into the packages dir in the correct
    #          branch, no package must be added into the package database and
    #          the events must be issued to the view properly.

    #    """
    #    master_repo_names = ['foo-repo', 'bar-repo', 'qux-repo']
    #    master_branch_name = 'master'
    #    master_user = 'fake_user'
    #    repo_urls = [
    #        'https://github.com/{}/{}.git'.format(master_user, master_repo_names[0]),
    #        'https://github.com/{}/{}.git'.format(master_user, master_repo_names[1]),
    #        'https://github.com/{}/{}.git'.format(master_user, master_repo_names[2])
    #    ]
    #    master_repo_ids = [
    #        '{}/{}'.format(master_user, master_repo_names[0]),
    #        '{}/{}'.format(master_user, master_repo_names[1]),
    #        '{}/{}'.format(master_user, master_repo_names[2])
    #    ]

    #    with open('/etc/gur/mirrors.csv', 'w') as mirrors:
    #        mirrors.truncate(0)
    #        for i in range(len(repo_urls)):
    #            mirrors.write('{},{}\n'.format(master_branch_name, repo_urls[i]))

    #    listdir_mock.return_value = []
    #    isdir_mock.return_value = True

    #    cmd = UpdateCmd(pkg_mgr_mock)
    #    cmd.execute(listener_mock)

    #    listener_mock.assert_has_calls(
    #        [
    #            call.on_update_start(),

    #            call.on_repo_update_start(master_repo_ids[0], master_branch_name),
    #            call.on_update_progress(1, 0, 1, 'Pulling master repo ...'),
    #            call.on_update_progress(1, 1, 1, 'Pulling master repo ...'),
    #            call.on_repo_update_finish(master_repo_ids[0], master_branch_name),

    #            call.on_repo_update_start(master_repo_ids[1], master_branch_name),
    #            call.on_update_progress(1, 0, 1, 'Pulling master repo ...'),
    #            call.on_update_progress(1, 1, 1, 'Pulling master repo ...'),
    #            call.on_repo_update_finish(master_repo_ids[1], master_branch_name),

    #            call.on_repo_update_start(master_repo_ids[2], master_branch_name),
    #            call.on_update_progress(1, 0, 1, 'Pulling master repo ...'),
    #            call.on_update_progress(1, 1, 1, 'Pulling master repo ...'),
    #            call.on_repo_update_finish(master_repo_ids[2], master_branch_name),

    #            call.on_update_finish()
    #        ]
    #    )

    #    listener_mock.on_pkg_update_start.assert_not_called()
    #    listener_mock.on_pkg_update_finish.assert_not_called()
    #    pkg_mgr_mock.switch_dir.assert_called_once()
    #    pkg_mgr_mock.update_entry.assert_not_called()

    #    git_mock.assert_has_calls(
    #        [
    #            call(master_repo_ids[0]),
    #            call().remotes.origin.pull(master_branch_name),

    #            call(master_repo_ids[1]),
    #            call().remotes.origin.pull(master_branch_name),

    #            call(master_repo_ids[2]),
    #            call().remotes.origin.pull(master_branch_name)
    #        ]
    #    )

    #    git_mock.init.assert_not_called()
    #    git_mock.init.create_remote.assert_not_called()
    #    git_mock.init.create_remote.fetch.assert_not_called()

    ## TODO: multiple users
    ## TODO: errors

if __name__ == "__main__":
    main()
