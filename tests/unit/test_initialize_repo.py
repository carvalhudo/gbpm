from unittest import TestCase, main
from unittest.mock import patch, call, ANY

from errors import error_map
from os import chdir
import git

from commands import UpdateCmd

class InitializeRepoTest(TestCase):

    """
    Implementation of unit tests for initialize repo command.

    """
    def setUpClass():
        chdir('resources/')

    def tearDownClass():
        chdir('../')

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_initialize_repo_with_single_package(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock,
        mirrors_mock):
        """
        GIVEN the package dir is empty and the mirrors file contains only one
              repo.
        WHEN  the user issues an Update/InitializeRepo command.
        THEN  the repository must be cloned into the packages dir in the correct
              branch, the package must be added into the package database and
              the events must be issued to the view properly.

        """
        pkg_name = 'foo_pkg'
        pkg_branch = 'foo_branch'
        pkg_repo = 'foo_repo'
        master_repo_name = 'fake_repo_1'
        master_branch_name = 'master'
        master_user = 'fake_user'
        repo_url = 'https://github.com/{}/{}.git'.format(
            master_user,
            master_repo_name
        )
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        isdir_mock.return_value = False
        listdir_mock.return_value = [pkg_name]
        mirrors_mock.return_value = [
            '{},{}'.format(master_branch_name, repo_url)
        ]
        #git_mock().rev_parse.return_value = 'fake_hash'

        cmd = UpdateCmd.InitializeRepoCmd(
            pkg_mgr_mock,
            master_repo_id,
            master_branch_name,
            repo_url
        )
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_repo_update_start(master_repo_id, master_branch_name),
                call.on_update_progress(0, 0, 0, 'Cloning master repo ...'),
                call.on_repo_update_finish(master_repo_id, master_branch_name),
                call.on_pkg_update_start(pkg_name, pkg_branch),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_name)),
                call.on_pkg_update_finish(pkg_name, pkg_branch)
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.add_entry(
                    pkg_name,
                    ANY # TODO: 'fake_hash',
                )
            ]
        )

        git_mock.assert_has_calls(
            [
                call.clone_from(
                    repo_url,
                    master_repo_id,
                    branch=master_branch_name,
                    progress=ANY
                ),
                call.init('{}/src/{}/.repo'.format(master_repo_id, pkg_name)),
                call.init().create_remote(
                    'origin',
                    pkg_repo
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branch))
            ]
        )

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_initialize_repo_with_multiple_packages(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock,
        mirrors_mock):
        """
        GIVEN the package dir is empty and the mirrors file contains only one
              repo which contains multiple packages.
        WHEN  the user issues an Update/InitializeRepo command.
        THEN  the repository must be cloned into the package dir in the correct
              branch, the packages must be added into the package database and
              the events must be issued to the view properly.

        """
        pkg_names = ['foo_pkg', 'bar_pkg', 'baz_pkg', 'qux_pkg']
        pkg_branches = ['foo_branch', 'bar_branch', 'baz_branch', 'qux_branch']
        pkg_repos = ['foo_repo', 'bar_repo', 'baz_repo', 'qux_repo']
        master_repo_name = 'fake_repo_1'
        master_branch_name = 'master'
        master_user = 'fake_user'
        repo_url = 'https://github.com/{}/{}.git'.format(
            master_user,
            master_repo_name
        )
        master_repo_id = '{}/{}'.format(master_user, master_repo_name)

        isdir_mock.return_value = False
        listdir_mock.return_value = pkg_names
        mirrors_mock.return_value = [
            '{},{}'.format(master_branch_name, repo_url)
        ]

        cmd = UpdateCmd.InitializeRepoCmd(
            pkg_mgr_mock,
            master_repo_id,
            master_branch_name,
            repo_url
        )
        cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_repo_update_start(master_repo_id, master_branch_name),
                call.on_update_progress(0, 0, 0, 'Cloning master repo ...'),
                call.on_repo_update_finish(master_repo_id, master_branch_name),
                call.on_pkg_update_start(pkg_names[0], pkg_branches[0]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[0])),
                call.on_pkg_update_finish(pkg_names[0], pkg_branches[0]),
                call.on_pkg_update_start(pkg_names[1], pkg_branches[1]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[1])),
                call.on_pkg_update_finish(pkg_names[1], pkg_branches[1]),
                call.on_pkg_update_start(pkg_names[2], pkg_branches[2]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[2])),
                call.on_pkg_update_finish(pkg_names[2], pkg_branches[2]),
                call.on_pkg_update_start(pkg_names[3], pkg_branches[3]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[3])),
                call.on_pkg_update_finish(pkg_names[3], pkg_branches[3]),
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.add_entry(
                    pkg_names[0],
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_names[1],
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_names[2],
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_names[3],
                    ANY # TODO
                )
            ],
        )

        git_mock.assert_has_calls(
            [
                call.clone_from(
                    repo_url,
                    master_repo_id,
                    branch=master_branch_name,
                    progress=ANY
                ),

                call.init('{}/src/{}/.repo'.format(master_repo_id, pkg_names[0])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[0]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[0])),

                call.init('{}/src/{}/.repo'.format(master_repo_id, pkg_names[1])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[1]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[1])),

                call.init('{}/src/{}/.repo'.format(master_repo_id, pkg_names[2])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[2]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[2])),

                call.init('{}/src/{}/.repo'.format(master_repo_id, pkg_names[3])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[3]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[3]))
            ]
        )

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_initialize_multiple_repos_with_single_package(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock,
        mirrors_mock):
        """
        GIVEN the package dir is empty and the mirrors file contains
              multiple repos and each one of them contains only one package.
        WHEN  the user issues an Update/InitializeRepo command.
        THEN  the repository must be cloned into the package dir in the
              correct branch, the package must be added into the package
              database for every repo and the events must be issued to the
              view properly.

        """
        pkg_name = 'foo_pkg'
        pkg_branch = 'foo_branch'
        pkg_repo = 'foo_repo'
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
        listdir_mock.return_value = [pkg_name]
        mirrors_mock.return_value = [
            '{},{}\n'.format(master_branch_name, repo_urls[0]),
            '{},{}\n'.format(master_branch_name, repo_urls[1]),
            '{},{}\n'.format(master_branch_name, repo_urls[2])
        ]

        for i,_ in enumerate(master_repo_ids):
            cmd = UpdateCmd.InitializeRepoCmd(
                pkg_mgr_mock,
                master_repo_ids[i],
                master_branch_name,
                repo_urls[i]
            )
            cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_repo_update_start(master_repo_ids[0], master_branch_name),
                call.on_update_progress(0, 0, 0, 'Cloning master repo ...'),
                call.on_repo_update_finish(master_repo_ids[0], master_branch_name),
                call.on_pkg_update_start(pkg_name, pkg_branch),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_name)),
                call.on_pkg_update_finish(pkg_name, pkg_branch),

                call.on_repo_update_start(master_repo_ids[1], master_branch_name),
                call.on_update_progress(0, 0, 0, 'Cloning master repo ...'),
                call.on_repo_update_finish(master_repo_ids[1], master_branch_name),
                call.on_pkg_update_start(pkg_name, pkg_branch),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_name)),
                call.on_pkg_update_finish(pkg_name, pkg_branch),

                call.on_repo_update_start(master_repo_ids[2], master_branch_name),
                call.on_update_progress(0, 0, 0, 'Cloning master repo ...'),
                call.on_repo_update_finish(master_repo_ids[2], master_branch_name),
                call.on_pkg_update_start(pkg_name, pkg_branch),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_name)),
                call.on_pkg_update_finish(pkg_name, pkg_branch),
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.add_entry(
                    pkg_name,
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_name,
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_name,
                    ANY # TODO
                ),
            ],
        )

        git_mock.assert_has_calls(
            [
                call.clone_from(
                    repo_urls[0],
                    master_repo_ids[0],
                    branch=master_branch_name,
                    progress=ANY
                ),

                call.init('{}/src/{}/.repo'.format(master_repo_ids[0], pkg_name)),
                call.init().create_remote(
                    'origin',
                    pkg_repo
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branch)),

                call.clone_from(
                    repo_urls[1],
                    master_repo_ids[1],
                    branch=master_branch_name,
                    progress=ANY
                ),

                call.init('{}/src/{}/.repo'.format(master_repo_ids[1], pkg_name)),
                call.init().create_remote(
                    'origin',
                    pkg_repo
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branch)),

                call.clone_from(
                    repo_urls[2],
                    master_repo_ids[2],
                    branch=master_branch_name,
                    progress=ANY
                ),

                call.init('{}/src/{}/.repo'.format(master_repo_ids[2], pkg_name)),
                call.init().create_remote(
                    'origin',
                    pkg_repo
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branch))
            ]
        )

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_initialize_multiple_repos_with_multiple_packages(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock,
        mirrors_mock):
        """
        GIVEN the package dir is empty and the mirrors file contains
              multiple repos and each one of them contains multiple packages.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the
              correct branch, the packages must be added into the package
              database and the events must be issued to the view properly.

        """
        pkg_names = ['foo_pkg', 'bar_pkg', 'qux_pkg']
        pkg_branches = ['foo_branch', 'bar_branch', 'qux_branch']
        pkg_repos = ['foo_repo', 'bar_repo', 'qux_repo']
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
        listdir_mock.return_value = pkg_names
        mirrors_mock.return_value = [
            '{},{}\n'.format(master_branch_name, repo_urls[0]),
            '{},{}\n'.format(master_branch_name, repo_urls[1]),
            '{},{}\n'.format(master_branch_name, repo_urls[2])
        ]

        for i,_ in enumerate(master_repo_ids):
            cmd = UpdateCmd.InitializeRepoCmd(
                pkg_mgr_mock,
                master_repo_ids[i],
                master_branch_name,
                repo_urls[i]
            )
            cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_repo_update_start(master_repo_ids[0], master_branch_name),
                call.on_update_progress(0, 0, 0, 'Cloning master repo ...'),
                call.on_repo_update_finish(master_repo_ids[0], master_branch_name),
                call.on_pkg_update_start(pkg_names[0], pkg_branches[0]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[0])),
                call.on_pkg_update_finish(pkg_names[0], pkg_branches[0]),
                call.on_pkg_update_start(pkg_names[1], pkg_branches[1]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[1])),
                call.on_pkg_update_finish(pkg_names[1], pkg_branches[1]),
                call.on_pkg_update_start(pkg_names[2], pkg_branches[2]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[2])),
                call.on_pkg_update_finish(pkg_names[2], pkg_branches[2]),

                call.on_repo_update_start(master_repo_ids[1], master_branch_name),
                call.on_update_progress(0, 0, 0, 'Cloning master repo ...'),
                call.on_repo_update_finish(master_repo_ids[1], master_branch_name),
                call.on_pkg_update_start(pkg_names[0], pkg_branches[0]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[0])),
                call.on_pkg_update_finish(pkg_names[0], pkg_branches[0]),
                call.on_pkg_update_start(pkg_names[1], pkg_branches[1]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[1])),
                call.on_pkg_update_finish(pkg_names[1], pkg_branches[1]),
                call.on_pkg_update_start(pkg_names[2], pkg_branches[2]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[2])),
                call.on_pkg_update_finish(pkg_names[2], pkg_branches[2]),

                call.on_repo_update_start(master_repo_ids[2], master_branch_name),
                call.on_update_progress(0, 0, 0, 'Cloning master repo ...'),
                call.on_repo_update_finish(master_repo_ids[2], master_branch_name),
                call.on_pkg_update_start(pkg_names[0], pkg_branches[0]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[0])),
                call.on_pkg_update_finish(pkg_names[0], pkg_branches[0]),
                call.on_pkg_update_start(pkg_names[1], pkg_branches[1]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[1])),
                call.on_pkg_update_finish(pkg_names[1], pkg_branches[1]),
                call.on_pkg_update_start(pkg_names[2], pkg_branches[2]),
                call.on_update_progress(0, 0, 0, 'Fetching {} ...'.format(pkg_names[2])),
                call.on_pkg_update_finish(pkg_names[2], pkg_branches[2]),
            ]
        )

        pkg_mgr_mock.assert_has_calls(
            [
                call.add_entry(
                    pkg_names[0],
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_names[1],
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_names[2],
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_names[0],
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_names[1],
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_names[2],
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_names[0],
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_names[1],
                    ANY # TODO
                ),
                call.add_entry(
                    pkg_names[2],
                    ANY # TODO
                )
            ]
        )

        git_mock.assert_has_calls(
            [
                call.clone_from(
                    repo_urls[0],
                    master_repo_ids[0],
                    branch=master_branch_name,
                    progress=ANY
                ),
                call.init('{}/src/{}/.repo'.format(master_repo_ids[0], pkg_names[0])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[0]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[0])),

                call.init('{}/src/{}/.repo'.format(master_repo_ids[0], pkg_names[1])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[1]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[1])),

                call.init('{}/src/{}/.repo'.format(master_repo_ids[0], pkg_names[2])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[2]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[2])),

                call.clone_from(
                    repo_urls[1],
                    master_repo_ids[1],
                    branch=master_branch_name,
                    progress=ANY
                ),
                call.init('{}/src/{}/.repo'.format(master_repo_ids[1], pkg_names[0])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[0]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[0])),

                call.init('{}/src/{}/.repo'.format(master_repo_ids[1], pkg_names[1])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[1]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[1])),

                call.init('{}/src/{}/.repo'.format(master_repo_ids[1], pkg_names[2])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[2]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[2])),

                call.clone_from(
                    repo_urls[2],
                    master_repo_ids[2],
                    branch=master_branch_name,
                    progress=ANY
                ),
                call.init('{}/src/{}/.repo'.format(master_repo_ids[2], pkg_names[0])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[0]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[0])),

                call.init('{}/src/{}/.repo'.format(master_repo_ids[2], pkg_names[1])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[1]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[1])),

                call.init('{}/src/{}/.repo'.format(master_repo_ids[2], pkg_names[2])),
                call.init().create_remote(
                    'origin',
                    pkg_repos[2]
                ),
                call.init().create_remote().fetch(progress=ANY),
                call.init().rev_parse('origin/{}'.format(pkg_branches[2]))
            ]
        )

    @patch('mirrors_mgr.MirrorsMgr.get_mirrors')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('package_database_mgr.PackageDatabaseMgr')
    @patch('git.Repo')
    @patch('views.CliUpdateView')
    def test_initialize_multiple_repos_with_no_packages(
        self,
        listener_mock,
        git_mock,
        pkg_mgr_mock,
        listdir_mock,
        isdir_mock,
        mirrors_mock):
        """
        GIVEN the package dir is empty and the mirrors file contains
              multiple repos with no packages.
        WHEN  the user issues an update command.
        THEN  the repository must be cloned into the packages dir in the
              correct branch, no packages must be added into the package
              database and the events must be issued to the view properly.

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
        listdir_mock.return_value = []
        mirrors_mock.return_value = [
            '{},{}\n'.format(master_branch_name, repo_urls[0]),
            '{},{}\n'.format(master_branch_name, repo_urls[1]),
            '{},{}\n'.format(master_branch_name, repo_urls[2])
        ]

        for i,_ in enumerate(master_repo_ids):
            cmd = UpdateCmd.InitializeRepoCmd(
                pkg_mgr_mock,
                master_repo_ids[i],
                master_branch_name,
                repo_urls[i]
            )
            cmd.execute(listener_mock)

        listener_mock.assert_has_calls(
            [
                call.on_repo_update_start(master_repo_ids[0], master_branch_name),
                call.on_update_progress(0, 0, 0, 'Cloning master repo ...'),
                call.on_repo_update_finish(master_repo_ids[0], master_branch_name),
                call.on_repo_update_start(master_repo_ids[1], master_branch_name),
                call.on_update_progress(0, 0, 0, 'Cloning master repo ...'),
                call.on_repo_update_finish(master_repo_ids[1], master_branch_name),
                call.on_repo_update_start(master_repo_ids[2], master_branch_name),
                call.on_update_progress(0, 0, 0, 'Cloning master repo ...'),
                call.on_repo_update_finish(master_repo_ids[2], master_branch_name),
            ]
        )

        listener_mock.on_pkg_update_start.assert_not_called()
        listener_mock.on_pkg_update_finish.assert_not_called()
        pkg_mgr_mock.add_entry.assert_not_called()

        git_mock.assert_has_calls(
            [
                call.clone_from(
                    repo_urls[0],
                    master_repo_ids[0],
                    branch=master_branch_name,
                    progress=ANY
                ),
                call.clone_from(
                    repo_urls[1],
                    master_repo_ids[1],
                    branch=master_branch_name,
                    progress=ANY
                ),
                call.clone_from(
                    repo_urls[2],
                    master_repo_ids[2],
                    branch=master_branch_name,
                    progress=ANY
                )
            ]
        )

        git_mock.init.assert_not_called()
        git_mock.init.create_remote.assert_not_called()
        git_mock.init.create_remote.fetch.assert_not_called()

if __name__ == "__main__":
    main()
