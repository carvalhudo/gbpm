
class MirrorsMgr(object):

    """
    Class responsible for the management of the mirrors file of gbpm

    """

    def __init__(self):
        """
        Initialize the current class instance

        """
        self.__mirrors_file = '/etc/gbpm/mirrors.conf'

    def add_repo(self, repo_url):
        """
        Add a new package repository into the mirrors config file

        :repo_url: URL of package repository

        """
        with open(self.__mirrors_file, 'r+') as mirrors_file:
            conf_entry = f'{repo_url}\n'

            if conf_entry not in mirrors_file.readlines():
                mirrors_file.write(conf_entry)

    @property
    def mirrors_file(self):
        """
        Get the 'mirrors' filepath

        :returns: The absolute path of the file

        """
        return self.__mirrors_file
