from argparse import Action

from package_database_mgr import PackageDatabaseMgr

class UpdateAction(Action):

    """
    Class responsible for implementing the 'UpdateAction' action

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
        Execute the 'UpdateAction' action

        """
        db_mgr = PackageDatabaseMgr()

        db_mgr.update()
