from abc import ABC, abstractmethod

class ListPkgsListener(ABC):

    """
    Definition of the interface for the list-pkgs command events.

    """

    @abstractmethod
    def on_pkg_list_start(self, pkg_repo):
        """
        Trigger an on_pkg_list_start event, which indicates the start of list
        operation.

        :pkg_repo: Name of the package repository.

        """
        pass # pragma: no cover

    @abstractmethod
    def on_pkg_list_finish(self, pkg_repo):
        """
        Trigger an on_pkg_list_finish event, which indicates the end of list
        operation.

        :pkg_repo: Name of the package repository.

        """
        pass # pragma: no cover

    @abstractmethod
    def on_pkg_show(self, pkg_name, is_installed):
        """
        Trigger an on_pkg_show event, which indicates that a package was
        found.

        :pkg_name: Name of the package.
        :is_installed: True if the package is installed; otherwise False.

        """
        pass # pragma: no cover
