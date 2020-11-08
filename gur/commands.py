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
    Implementation for progress report for gur commands.

    """

    def __init__(self, listener, msg):
        """
        Initialize the internal data.

        """
        git.remote.RemoteProgress.__init__(self)

        self.listener = listener
        self.msg = msg

    def update(self, op_code, cur_count, max_count, msg):
        """Update the view with the current progress of the command.

        """
        self.listener.on_update_progress(op_code, cur_count, max_count, self.msg)

class UpdateCmd(Command):

    """
    Execute an update command. The main goal of this command is to sync the
    local database with the upstream data related to the gur packages.

    """

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

                listener.on_repo_update_start(repo_id, branch_name)

                if os.path.isdir(repo_id):
                    repo = git.Repo(repo_id)

                    listener.on_update_progress(1, 0, 1, 'Pulling master repo ...')
                    repo.remotes.origin.pull(branch_name)
                    listener.on_update_progress(1, 1, 1, 'Pulling master repo ...')

                    for pkg_entry in os.listdir(repo_id + '/src'):
                        pkg = PackageDesc(repo_id, pkg_entry)

                        listener.on_pkg_update_start(pkg.name, pkg.branch)
                        pkg_repo = git.Repo(pkg.dir)
                        pkg_repo.remotes.origin.fetch(
                            progress=CommandProgress(listener, 'Fetching {} ...'.format(pkg.name))
                        )

                        head_commit = pkg_repo.rev_parse(
                            'origin/{}'.format(pkg.branch)
                        )
                        self.pkg_mgr.update_entry(pkg.name, head_commit.hexsha)
                        listener.on_pkg_update_finish(pkg.name, pkg.branch)
                else:
                    _ = git.Repo.clone_from(
                        repo_url,
                        repo_id,
                        branch=branch_name,
                        progress=CommandProgress(listener, 'Cloning master repo ...')
                    )

                    for pkg_entry in os.listdir(repo_id + '/src'):
                        pkg = PackageDesc(repo_id, pkg_entry)

                        listener.on_pkg_update_start(pkg.name, pkg.branch)

                        pkg_repo = git.Repo.init(pkg.dir)
                        origin = pkg_repo.create_remote('origin', pkg.repo)
                        origin.fetch(
                            progress=CommandProgress(listener, 'Fetching {} ...'.format(pkg.name))
                        )

                        head_commit = pkg_repo.rev_parse(
                            'origin/{}'.format(pkg.branch)
                        )
                        self.pkg_mgr.add_entry(pkg.name, head_commit.hexsha)
                        listener.on_pkg_update_finish(pkg.name, pkg.branch)

                listener.on_repo_update_finish(repo_id, branch_name)
            except git.GitCommandError as err:
                error_msg = ''
                try:
                    error_msg = error_map[err.command[1]]
                except KeyError:
                    error_msg = error_map['unknown']

                listener.on_error(error_msg)

        listener.on_update_finish()
