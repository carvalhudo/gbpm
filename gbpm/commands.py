from abc import ABC, abstractmethod
import git
import os

from mirrors_mgr import MirrorsMgr
from package_database_mgr import PackageDatabaseMgr
from package_desc import PackageDesc
from utils import Utils

class Command(ABC):

    """
    Definition of the interface for gbpm commands.

    """

    @abstractmethod
    def execute(self, listener):
        """
        Definition of the command contract.

        :listener: Listener to report the command events.

        """
        pass

class UpdateCmd(Command):

    """
    Execute an update command. The main goal of this command is to sync the
    local database with the upstream data related to the gbpm packages.

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
                repo_name = Utils.get_repo_id(repo_url)

                listener.on_repo_update_start(repo_name, branch_name)

                if os.path.isdir(repo_name):
                    # verify for new packages in the repository
                    repo = git.Repo(repo_name)

                    listener.on_update_progress(1, 0, 1, '')
                    repo.remotes.origin.pull(branch_name)
                    listener.on_update_progress(1, 1, 1, '')

                    for pkg_entry in os.listdir(repo_name):
                        if pkg_entry == '.git':
                            continue

                        pkg = PackageDesc(repo_name, pkg_entry)

                        listener.on_pkg_update_start(pkg.name, pkg.branch)
                        pkg_repo = git.Repo(pkg.dir)
                        pkg_repo.remotes.origin.fetch(
                            progress=lambda op_code,
                                cur_count,
                                max_count,
                                msg: listener.on_update_progress(op_code, cur_count, max_count, msg)
                        )

                        head_commit = pkg_repo.rev_parse(
                            'origin/{}'.format(pkg.branch)
                        )
                        self.pkg_mgr.update_entry(pkg.name, head_commit.hexsha)
                        listener.on_pkg_update_finish(pkg.name, pkg.branch)
                else:
                    _ = git.Repo.clone_from(
                        repo_url,
                        repo_name,
                        branch=branch_name,
                        progress=lambda op_code,
                            cur_count,
                            max_count,
                            msg: listener.on_update_progress(op_code, cur_count, max_count, msg)
                    )

                    for pkg_entry in os.listdir(repo_name):
                        if pkg_entry == '.git':
                            continue

                        pkg = PackageDesc(repo_name, pkg_entry)

                        listener.on_pkg_update_start(pkg.name, pkg.branch)

                        pkg_repo = git.Repo.init(pkg.dir)
                        origin = pkg_repo.create_remote('origin', pkg.repo)
                        origin.fetch(
                            progress=lambda op_code,
                                cur_count,
                                max_count,
                                msg: listener.on_update_progress(op_code, cur_count, max_count, msg)
                        )

                        head_commit = pkg_repo.rev_parse(
                            'origin/{}'.format(pkg.branch)
                        )
                        self.pkg_mgr.add_entry(pkg.name, head_commit.hexsha)
                        listener.on_pkg_update_finish(pkg.name, pkg.branch)

                listener.on_repo_update_finish(repo_name, branch_name)
            except Exception as e:
                listener.on_error(e)
                continue

        listener.on_update_finish()
