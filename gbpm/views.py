from update_listener import UpdateListener

from tqdm import tqdm
from package_database_mgr import PackageDatabaseMgr

class CliUpdateView(UpdateListener):

    """Docstring for View. """

    def __init__(self):
        """TODO: to be defined. """
        UpdateListener.__init__(self)

        self.db_mgr = PackageDatabaseMgr()
        self.prog_bar = None

    def update(self):
        """TODO: Docstring for update.
        :returns: TODO

        """
        self.db_mgr.update(self)

    def on_update_start(self):
        """
        Trigger an update_start event, which indicates that a update
        operation has started.

        """
        print('Updating local database ...\n')

    def on_update_finish(self):
        """
        Trigger an update_finish event, which indicates that a update
        operation has finished.

        """
        pass

    def on_repo_update_start(self, repo_name, branch_name):
        """
        Trigger an repo_update_start event, which indicates that a update
        operation for a given repository has started.

        :repo_name: Name of the repository which will be updated.

        """
        max_repo_name = 15
        name = repo_name + (max_repo_name - len(repo_name)) * ' '

        self.prog_bar = tqdm(
            desc=name,
            bar_format=
                '    {desc:<6.15}: {percentage:3.0f}% |{bar:50}|' +
                ' [{elapsed}/{remaining}]'
        )

    def on_repo_update_finish(self, repo_name, branch_name):
        """
        Trigger an repo_update_finish event, which indicates that a update
        operation for a given repository has finished.

        :repo_name: Name of the repository which will be updated.

        """
        self.prog_bar.close()

    def on_update_progress(self, op_code, cur_count, max_count, msg):
        """
        Trigger an update_progress event, which reports the current progress
        of the update operation.

        :curr_progress: current progress.

        """
        if self.prog_bar.total != max_count:
            self.prog_bar.total = max_count

        self.prog_bar.n = cur_count
        self.prog_bar.refresh()

    def on_error(self, msg):
        """
        Trigger an error event, which reports an error for the
        update operation.

        :msg: The error message.

        """
        print(msg)
