from abc import ABC, abstractmethod
from re import search

class GitAppBase(ABC):

    """Docstring for GitAppBase. """

    def __init__(self, repo, app_name):
        """
        TODO: to be defined.

        """
        self._repo = repo
        self._app_name = app_name

    def get_repo_name(self):
        """
        TODO: Docstring for repo_name.
        :returns: TODO

        """
        pattern_list = [
            f'https://{self._app_name}.com/(.+?).git',
            f'git@{self._app_name}.com:(.+?).git'
        ]

        repo_name = ''
        for pattern in pattern_list:
            ret = search(pattern, self._repo)

            if ret:
                repo_name = ret.group(1)
                break

        return repo_name

    @abstractmethod
    def clone(self, **kwargs):
        """TODO: Docstring for clone.
        :returns: TODO

        """
        pass

    @abstractmethod
    def pull(self):
        """TODO: Docstring for pull.
        :returns: TODO

        """
        # use -C option of git
        pass

    def is_repo_https(self):
        """TODO: Docstring for is_repo_https.
        :returns: TODO

        """
        pass
