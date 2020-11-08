from tqdm import tqdm

from os import get_terminal_size
from commands import UpdateCmd
from update_listener import UpdateListener

class CliUpdateView:

    """
    Implementation of update view.

    """

    class EventHandler(UpdateListener):

        """
        Implementation of the event handler class, which will be responsible to
        receive the operation events and propagate them to the view.

        """

        def __init__(self, view):
            """
            Initialize the event handler internal data.

            """
            super().__init__()

            self.view = view

        def on_update_start(self):
            """
            Trigger an update_start event, which indicates that a update
            operation has started.

            """
            self.view.on_update_start()

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
            self.view.on_repo_update_start(repo_name, branch_name)

        def on_repo_update_finish(self, repo_name, branch_name):
            """
            Trigger an repo_update_finish event, which indicates that a update
            operation for a given repository has finished.

            :repo_name: Name of the repository which will be updated.
            :branch_name: Name of the branch.

            """
            self.view.on_repo_update_finish(repo_name, branch_name)

        def on_master_repo_update_start(self, repo_name, branch_name):
            """
            Trigger an master_repo_update_start event, which indicates that a update
            operation for a master repository has started.

            :repo_name: Name of the repository which will be updated.
            :branch_name: Name of the branch.

            """
            pass

        def on_master_repo_update_finish(self, repo_name, branch_name):
            """
            Trigger an master_repo_update_finish event, which indicates that a
            update operation for a master repository has finished.

            :repo_name: Name of the repository which will be updated.
            :branch_name: Name of the branch.

            """
            self.view.on_master_repo_update_finish(repo_name, branch_name)

        def on_pkg_update_start(self, pkg_name, branch_name):
            """
            Trigger an pkg_update_start event, which indicates that a update
            operation for an individual package has started.

            :pkg_name: Name of the package which will be updated.
            :branch_name: Name of the branch.

            """
            self.view.on_pkg_update_start(pkg_name, branch_name)

        def on_pkg_update_finish(self, pkg_name, branch_name):
            """
            Trigger an pkg_update_finish event, which indicates that a update
            operation for an individual package has finished.

            :pkg_name: Name of the package which will be updated.
            :branch_name: Name of the branch.

            """
            self.view.on_pkg_update_finish(pkg_name, branch_name)

        def on_update_progress(self, op_code, cur_count, max_count, msg):
            """
            Trigger an update_progress event, which reports the current progress
            of the update operation.

            """
            self.view.on_update_progress(op_code, cur_count, max_count, msg)

        def on_error(self, msg):
            """
            Trigger an error event, which reports an error for the
            update operation.

            :msg: The error message.

            """
            self.view.on_error(msg)

    def __init__(self):
        """
        Initialize the update view internal data.

        """
        self.cmd = UpdateCmd()
        self.event_handler = CliUpdateView.EventHandler(self)
        self.prog_bar = None

    def update(self):
        """
        Trigger the update command.

        """
        self.cmd.execute(self.event_handler)

    def on_update_start(self):
        """
        Trigger an update_start event, which indicates that a update
        operation has started.

        """
        print('Updating local database ...\n')

    def on_repo_update_start(self, repo_name, branch_name):
        """
        Trigger an repo_update_start event, which indicates that a update
        operation for a given repository has started.

        :repo_name: Name of the repository which will be updated.
        :branch_name: Name of the branch.

        """
        bar_width = int(get_terminal_size().columns * 0.3)

        self.prog_bar = tqdm(
            bar_format=
                '    {percentage:3.0f}% |{bar:' + str(bar_width) + '}|' +
                ' [{elapsed}/{remaining}]{desc}'
        )
        self.prog_bar.write('{} from {} branch'.format(repo_name, branch_name))

    def on_repo_update_finish(self, repo_name, branch_name):
        """
        Trigger an repo_update_finish event, which indicates that a update
        operation for a given repository has finished.

        :repo_name: Name of the repository which will be updated.
        :branch_name: Name of the branch.

        """
        self.prog_bar.set_description_str(self.prog_bar.desc + ' OK')
        self.prog_bar.close()
        self.prog_bar = None

    def on_master_repo_update_finish(self, repo_name, branch_name):
        """
        Trigger an master_repo_update_finish event, which indicates that a
        update operation for a master repository has finished.

        :repo_name: Name of the repository which will be updated.
        :branch_name: Name of the branch.

        """
        print('')

    def on_pkg_update_start(self, pkg_name, branch_name):
        """
        Trigger an pkg_update_start event, which indicates that a update
        operation for an individual package has started.

        :pkg_name: Name of the package which will be updated.
        :branch_name: Name of the branch.

        """
        bar_width = int(get_terminal_size().columns * 0.3)

        self.prog_bar = tqdm(
            bar_format=
                '    {percentage:3.0f}% |{bar:' + str(bar_width) + '}|' +
                ' [{elapsed}/{remaining}]{desc}'
        )

    def on_pkg_update_finish(self, pkg_name, branch_name):
        """
        Trigger an pkg_update_finish event, which indicates that a update
        operation for an individual package has finished.

        :pkg_name: Name of the package which will be updated.
        :branch_name: Name of the branch.

        """
        self.prog_bar.set_description_str(self.prog_bar.desc + ' OK')
        self.prog_bar.close()
        self.prog_bar = None

    def on_update_progress(self, op_code, cur_count, max_count, msg):
        """
        Trigger an update_progress event, which reports the current progress
        of the update operation.

        """
        if self.prog_bar.total != max_count:
            self.prog_bar.total = max_count
            self.prog_bar.set_description_str(' ' + msg)

        self.prog_bar.n = cur_count
        self.prog_bar.refresh()

    def on_error(self, msg):
        """
        Trigger an error event, which reports an error for the
        update operation.

        :msg: The error message.

        """
        self.prog_bar.set_description_str(self.prog_bar.desc + ' ERROR: ' + msg)
        self.prog_bar.close()
        self.prog_bar = None

        print('')
