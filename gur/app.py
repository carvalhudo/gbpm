from views import CliUpdateView

class App:

    """
    Implementation of the main class of the App.

    """

    def __init__(self, args):
        """
        Initialize the app internal data.

        :args: Command line arguments.

        """
        self.args = args

    def run(self):
        """
        Run the app according to the specified args.

        """
        if self.args.update:
            view = CliUpdateView()
            view.update()
