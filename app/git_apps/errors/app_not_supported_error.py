
class AppNotSupportedError(Exception):

    """Docstring for AppNotSupportedError. """

    def __init__(self, repo_url):
        """TODO: to be defined. """
        self.__repo_url = repo_url

    def __str__(self):
        """TODO: Docstring for __str__.
        :returns: TODO

        """
        return f'the repository {self.__repo_url} is not supported!'
