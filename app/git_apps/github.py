from git_apps.git_app_base import GitAppBase

class Github(GitAppBase):

    """Docstring for Github. """

    def __init__(self, repo):
        """TODO: to be defined. """
        super().__init__(repo, 'github')
