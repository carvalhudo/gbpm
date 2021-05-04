from abc import ABC, abstractmethod

class UpdateListener(ABC):

    """
    Definition of the interface for for update command events.

    """

    @abstractmethod
    def on_update_start(self):
        """
        Trigger an update_start event, which indicates that a update
        operation has started.

        """
        pass # pragma: no cover

    @abstractmethod
    def on_update_finish(self):
        """
        Trigger an update_finish event, which indicates that a update
        operation has finished.

        """
        pass # pragma: no cover

    @abstractmethod
    def on_repo_update_start(self, repo_name, branch_name):
        """
        Trigger an repo_update_start event, which indicates that a update
        operation for a given repository has started.

        :repo_name: Name of the repository which will be updated.
        :branch_name: Name of the branch.

        """
        pass # pragma: no cover

    @abstractmethod
    def on_repo_update_finish(self, repo_name, branch_name):
        """
        Trigger an repo_update_finish event, which indicates that a update
        operation for a given repository has finished.

        :repo_name: Name of the repository which will be updated.
        :branch_name: Name of the branch.

        """
        pass # pragma: no cover

    @abstractmethod
    def on_pkg_update_start(self, pkg_name, branch_name):
        """
        Trigger an pkg_update_start event, which indicates that a update
        operation for an individual package has started.

        :pkg_name: Name of the package which will be updated.
        :branch_name: Name of the branch.

        """
        pass # pragma: no cover

    @abstractmethod
    def on_pkg_update_finish(self, pkg_name, branch_name):
        """
        Trigger an pkg_update_finish event, which indicates that a update
        operation for an individual package has finished.

        :pkg_name: Name of the package which will be updated.
        :branch_name: Name of the branch.

        """
        pass # pragma: no cover

    @abstractmethod
    def on_update_progress(self, op_code, cur_count, max_count, msg):
        """
        Trigger an update_progress event, which reports the current progress
        of the update operation.

        """
        pass # pragma: no cover

    @abstractmethod
    def on_error(self, msg):
        """
        Trigger an error event, which reports an error for the
        update operation.

        :msg: The error message.

        """
        pass # pragma: no cover
