from os.path import isfile

class MirrorsMgr:

    """
    Class responsible for the management of the mirrors file of gbpm

    """

    def __init__(self):
        """
        Initialize the current class instance

        """
        self.__mirrors_file = '/etc/gbpm/mirrors.conf'

        if not isfile(self.__mirrors_file):
            raise FileNotFoundError(
                f"the config file '{self.__mirrors_file}' was not found!"
            )

    def add_repo(self, repo_url):
        """
        Add a new package repository into the mirrors config file

        :repo_url: URL of package repository

        """
        with open(self.__mirrors_file, 'r+') as mirrors_file:
            mirror_entry = f'{repo_url}\n'

            if mirror_entry not in mirrors_file.readlines():
                mirrors_file.write(mirror_entry)

    def del_repo(self, repo_url):
        """
        Delete an existing package repository from mirrors config file

        :repo_url: URL of package repository

        """
        with open(self.__mirrors_file, 'r+') as mirrors_file:
            mirror_entry = f'{repo_url}\n'
            mirrors = mirrors_file.readlines()

            if not mirror_entry in mirrors:
                raise RuntimeError(
                    f'the repository {repo_url} was not previously configured!'
                )

            idx = mirrors.index(mirror_entry)
            del mirrors[idx]

            mirrors_file.seek(0)
            mirrors_file.truncate()
            mirrors_file.writelines(mirrors)

    @property
    def mirrors_file(self):
        """
        Get the 'mirrors' filepath

        :returns: The absolute path of the file

        """
        return self.__mirrors_file
