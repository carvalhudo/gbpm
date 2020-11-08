from git_apps.github import Github
from git_apps.errors.app_not_supported_error import AppNotSupportedError

class GitAppFactory:

    """Docstring for GitAppFactory. """

    @staticmethod
    def build(repo_url):
        """

        """
        if 'github' in repo_url:
            return Github(repo_url)

        raise AppNotSupportedError(repo_url)
