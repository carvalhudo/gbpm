from abc import ABC, abstractmethod

import git
import os

from errors import error_map
from mirrors_mgr import MirrorsMgr
from package_database_mgr import PackageDatabaseMgr
from package_desc import PackageDesc
from utils import Utils

class Command(ABC):

    """
    Definition of the interface for gur commands.

    """

    @abstractmethod
    def execute(self, listener):
        """
        Definition of the command contract.

        :listener: Listener to report the command events.

        """
        pass

class CommandProgress(git.remote.RemoteProgress):

    """
    Implementation of the class responsible for the progress reporting of gur
    commands.

    """

    def __init__(self, listener, cmd_desc):
        """
        Initialize the internal data.

        """
        super().__init__()

        self.listener = listener
        self.cmd_desc = cmd_desc

        # marking the start of the command
        self.update(0, 0, 0, self.cmd_desc)

    def __del__(self):
        """
        Marks the end of the command.

        """
        # when the local repository is synchronized with the upstream, the
        # update function is not triggered, so we must to mark the end of the
        # command to set the progress bar level to 100 %.
        self.update(1, 1, 1, self.cmd_desc)

    def update(self, op_code, cur_count, max_count, *_):
        """
        Update the view with the current progress of the command.

        """
        self.listener.on_update_progress(
            op_code,
            cur_count,
            max_count,
            self.cmd_desc
        )

class UpdateCmd(Command):

    """
    Implementation of 'Update' command. The main goal of this command is to
    sync the local database with the upstream repositories.

    """

    class InitializeRepoCmd(Command):

        """
        Implementation of InitializeRepo subcommand, responsible for the
        initialization of a new package repository.

        """

        def __init__(self, pkg_mgr, repo_id, branch_name, repo_url):
            """
            Initialize the command internal data.

            :pkg_mgr: Package manager instance.
            :repo_id: Identification of the repository.
            :branch_name: Name of the repository branch.
            :repo_url: Url of the repository.

            """
            super().__init__()

            self.pkg_mgr = pkg_mgr
            self.repo_id = repo_id
            self.branch_name = branch_name
            self.repo_url = repo_url

        def execute(self, listener):
            """
            Run the command.

            :listener: Event listener to propagate the command events.

            """
            listener.on_repo_update_start(self.repo_id, self.branch_name)

            _ = git.Repo.clone_from(
                self.repo_url,
                self.repo_id,
                branch=self.branch_name,
                progress=CommandProgress(listener, 'Cloning master repo ...')
            )

            listener.on_repo_update_finish(self.repo_id, self.branch_name)

            for pkg_entry in os.listdir(self.repo_id + '/src'):
                pkg = PackageDesc(self.repo_id, pkg_entry)

                listener.on_pkg_update_start(pkg.name, pkg.branch)

                pkg_repo = git.Repo.init(pkg.dir)
                origin = pkg_repo.create_remote('origin', pkg.repo)
                origin.fetch(
                    progress=CommandProgress(
                        listener,
                        'Fetching {} ...'.format(pkg.name)
                    )
                )

                head_commit = pkg_repo.rev_parse('origin/{}'.format(pkg.branch))
                self.pkg_mgr.add_entry(pkg.name, head_commit.hexsha)
                listener.on_pkg_update_finish(pkg.name, pkg.branch)

    class UpdateRepoCmd(Command):

        """
        Implementation of UpdateRepo subcommand, responsible for updating a new
        package repository.

        """

        def __init__(self, pkg_mgr, repo_id, branch_name):
            """
            Initialize the command internal data.

            """
            super().__init__()

            self.pkg_mgr = pkg_mgr
            self.repo_id = repo_id
            self.branch_name = branch_name

        def execute(self, listener):
            """
            Run the command.

            :listener: Event listener to propagate the command events.

            """
            listener.on_repo_update_start(self.repo_id, self.branch_name)

            repo = git.Repo(self.repo_id)

            listener.on_update_progress(1, 0, 1, 'Pulling master repo ...')
            repo.remotes.origin.pull(self.branch_name)
            listener.on_update_progress(1, 1, 1, 'Pulling master repo ...')

            listener.on_repo_update_finish(self.repo_id, self.branch_name)

            for pkg_entry in os.listdir(self.repo_id + '/src'):
                pkg = PackageDesc(self.repo_id, pkg_entry)
                pkg_repo = None

                listener.on_pkg_update_start(pkg.name, pkg.branch)

                # new package for an existing repo
                if not os.path.isdir(pkg.dir):
                    os.mkdir(pkg.dir)

                    pkg_repo = git.Repo.init(pkg.dir)
                    origin = pkg_repo.create_remote('origin', pkg.repo)
                    origin.fetch(
                        progress=CommandProgress(
                            listener,
                            'Fetching {} ...'.format(pkg.name)
                        )
                    )

                    head_commit = pkg_repo.rev_parse('origin/{}'.format(pkg.branch))
                    self.pkg_mgr.add_entry(pkg.name, head_commit.hexsha)
                else:
                    pkg_repo = git.Repo(pkg.dir)
                    pkg_repo.remotes.origin.fetch(
                        progress=CommandProgress(
                            listener,
                            'Fetching {} ...'.format(pkg.name)
                        )
                    )

                    head_commit = pkg_repo.rev_parse('origin/{}'.format(pkg.branch))
                    self.pkg_mgr.update_entry(pkg.name, head_commit.hexsha)

                listener.on_pkg_update_finish(pkg.name, pkg.branch)

    def __init__(self, pkg_mgr=None):
        """
        Initialize the command dependencies.

        """
        self.pkg_mgr = PackageDatabaseMgr() if not pkg_mgr else pkg_mgr

    def execute(self, listener):
        """
        Execute the update command.

        :listener: Listener to report the command events.

        """
        self.pkg_mgr.switch_dir()

        listener.on_update_start()
        for repo_entry in MirrorsMgr.get_mirrors():
            try:
                branch_name,repo_url = repo_entry.split(',')
                repo_id = Utils.get_repo_id(repo_url)
                inner_cmd = None

                listener.on_master_repo_update_start(
                    repo_id,
                    branch_name
                )

                if os.path.isdir(repo_id):
                    inner_cmd = UpdateCmd.UpdateRepoCmd(
                        self.pkg_mgr,
                        repo_id,
                        branch_name
                    )
                else:
                    inner_cmd = UpdateCmd.InitializeRepoCmd(
                        self.pkg_mgr,
                        repo_id,
                        branch_name,
                        repo_url
                    )

                inner_cmd.execute(listener)

                listener.on_master_repo_update_finish(
                    repo_id,
                    branch_name
                )
            except git.GitCommandError as err:
                listener.on_update_progress(1, 1, 1, '')
                listener.on_error(
                    '{} {}'.format(error_map[err.command[1]], repo_id)
                )
            except Exception:
                listener.on_update_progress(1, 1, 1, '')
                listener.on_error(error_map['unknown'])

        listener.on_update_finish()
