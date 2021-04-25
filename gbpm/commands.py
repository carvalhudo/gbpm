from abc import ABC, abstractmethod
import os
import git

from mirrors_mgr import MirrorsMgr
from package_database_mgr import PackageDatabaseMgr
from utils import Utils

class Command(ABC):

    """Docstring for Command. """

    @abstractmethod
    def execute(self, listener):
        """TODO: Docstring for execute.

        :f: TODO
        :returns: TODO

        """
        pass

class UpdateCmd(Command):

    """Docstring for UpdateCmd. """

    def __init__(self, pkg_mgr=None):
        """TODO: to be defined. """
        self.pkg_mgr = PackageDatabaseMgr() if not pkg_mgr else pkg_mgr

    def execute(self, listener):
        """TODO: Docstring for execute.
        :returns: TODO

        """

        self.pkg_mgr.switch_dir()

        listener.on_update_start()
        for repo_entry in MirrorsMgr.get_mirrors():
            try:
                branch_name,repo_url = repo_entry.split(',')
                repo_name = Utils.get_repo_name(repo_url)

                listener.on_repo_update_start(repo_name, branch_name)

                if os.path.isdir(repo_name):
                    # verify for new packages in the repository
                    repo = git.Repo(repo_name)

                    listener.on_update_progress(1, 0, 1, '')
                    repo.remotes.origin.pull(branch_name)
                    listener.on_update_progress(1, 1, 1, '')

                    for entry in os.listdir(repo_name):
                        if entry != '.git':
                            # update local database
                            self.pkg_mgr.update_entry(entry, repo_name)
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

                    for entry in os.listdir(repo_name):
                        if entry != '.git':
                            self.pkg_mgr.add_entry(entry, repo_name)

                listener.on_repo_update_finish(repo_name, branch_name)
            except Exception as e:
                listener.on_error(e)
                continue

        listener.on_update_finish()
