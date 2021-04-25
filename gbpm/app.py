from views import CliUpdateView

class App(object):

    """Docstring for App. """

    def __init__(self, args):
        """TODO: to be defined. """
        self.args = args

    def run(self):
        """
        Main routine of the app.

        """
        if self.args.update:
            view = CliUpdateView()
            view.update()
