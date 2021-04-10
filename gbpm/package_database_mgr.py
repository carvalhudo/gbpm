from os import chdir
from os.path import isdir
import git

from mirrors_mgr import MirrorsMgr
from utils import Utils

class PackageDatabaseMgr:

    """
    Docstring for PackageDatabaseMgr.

    """

    def __init__(self):
        """
        TODO: to be defined.

        """
        #self.pkg_dir = "/var/db/gbpm/"
        self.pkg_dir = "db/"
        self.db_file = "pkg_db.json"

        if not isdir(self.pkg_dir):
            raise RuntimeError(
                f"the package dir '{self.pkg_dir}' was not found!"
            )

    def update(self, listener):
        """
        TODO: Docstring for update.
        :returns: TODO

        """

        chdir(self.pkg_dir)

        listener.on_update_start()
        for repo_entry in MirrorsMgr.get_mirrors():
            try:
                branch_name,repo_url = repo_entry.split(',')
                repo_name = Utils.get_repo_name(repo_url)

                listener.on_repo_update_start(repo_name, branch_name)

                if isdir(repo_name):
                    repo = git.Repo(repo_name)

                    listener.on_update_progress(1, 0, 1, '')
                    repo.remotes.origin.pull(branch_name)
                    listener.on_update_progress(1, 1, 1, '')
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

                listener.on_repo_update_finish(repo_name, branch_name)
            except Exception as e:
                listener.on_error(e)
                continue

        listener.on_update_finish()
