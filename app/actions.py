from argparse import Action

from mirrors_mgr import MirrorsMgr

class AddPkgRepositoryAction(Action):

    """
    Class responsible for implementing the 'AddPkgRepository' action

    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """
        Initialize the current class instance

        """
        super(AddPkgRepositoryAction, self).__init__(
            option_strings,
            dest,
            **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        """
        Execute the 'AddPkgRepository' action

        """
        mgr = MirrorsMgr()

        mgr.add_repo(values)

class DelPkgRepositoryAction(Action):

    """
    Class responsible for implementing the 'DelPkgRepository' action

    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """
        Initialize the current class instance

        """
        super(DelPkgRepositoryAction, self).__init__(
            option_strings,
            dest,
            **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        """
        Execute the 'DelPkgRepository' action

        """
        mgr = MirrorsMgr()

        mgr.del_repo(values)
