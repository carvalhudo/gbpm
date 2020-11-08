from tqdm import tqdm

from commands import UpdateCmd
from update_listener import UpdateListener

class CliUpdateView(UpdateListener):

    """
    Implementation of update view.

    """

    def __init__(self):
        """
        Initialize the update view internal data.

        """
        UpdateListener.__init__(self)

        self.cmd = UpdateCmd()
        self.prog_bar = None

    def update(self):
        """
        Trigger the update command.

        """
        self.cmd.execute(self)

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
        :branch_name: Name of the branch.

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
        :branch_name: Name of the branch.

        """
        self.prog_bar.close()

    def on_pkg_update_start(self, pkg_name, branch_name):
        """
        Trigger an pkg_update_start event, which indicates that a update
        operation for an individual package has started.

        :pkg_name: Name of the package which will be updated.
        :branch_name: Name of the branch.

        """
        pass

    def on_pkg_update_finish(self, pkg_name, branch_name):
        """
        Trigger an pkg_update_finish event, which indicates that a update
        operation for an individual package has finished.

        :pkg_name: Name of the package which will be updated.
        :branch_name: Name of the branch.

        """
        pass

    def on_update_progress(self, op_code, cur_count, max_count, msg):
        """
        Trigger an update_progress event, which reports the current progress
        of the update operation.

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
