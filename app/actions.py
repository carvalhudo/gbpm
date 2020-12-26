from argparse import Action

from mirrors_mgr import MirrorsMgr
from validators import add_repo_validator

class AddPkgRepositoryAction(Action):

    """
    Class responsible for implementing the 'AddPkgRepository' action

    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """
        Initialize the current class instance

        """
        super().__init__(
            option_strings,
            dest,
            **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        """
        Execute the 'AddPkgRepository' action

        """
        if not add_repo_validator(values):
            raise ValueError('Error: invalid repo format.')

        branch,repo = values.split(':', 1)
        MirrorsMgr().add_repo(repo, branch)

class DelPkgRepositoryAction(Action):

    """
    Class responsible for implementing the 'DelPkgRepository' action

    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """
        Initialize the current class instance

        """
        super().__init__(
            option_strings,
            dest,
            **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        """
        Execute the 'DelPkgRepository' action

        """
        branch,repo = values.split(':', 1)

        MirrorsMgr().del_repo(repo, branch)
