from abc import ABC, abstractmethod

class UpdateListenter(ABC):

    """
    Listener for update command.

    """

    @abstractmethod
    def on_update_start(self):
        """
        Trigger an update_start event, which indicates that a update
        operation has started.

        """
        pass

    @abstractmethod
    def on_update_finish(self):
        """
        Trigger an update_finish event, which indicates that a update
        operation has finished.

        """
        pass

    @abstractmethod
    def on_repo_update_start(self):
        """
        Trigger an repo_update_start event, which indicates that a update
        operation for a given repository has started.

        """
        pass

    @abstractmethod
    def on_repo_update_finish(self):
        """
        Trigger an repo_update_finish event, which indicates that a update
        operation for a given repository has finished.

        """
        pass

    @abstractmethod
    def on_update_progress(self, curr_progress):
        """
        Trigger an update_progress event, which reports the current progress
        of the update operation.

        :curr_progress: current progress.

        """
        pass
