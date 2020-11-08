from json import load

class PackageDesc:

    """
    Implementation of the class responsible to represent a pkg_desc.json file.

    """

    def __init__(self, parent_repo, pkg_name):
        """
        Initialize the package description internal data.

        """
        desc_file = '{}/{}/pkg_desc.json'.format(
            parent_repo,
            pkg_name
        )

        self.__name = ''
        self.__branch = ''
        self.__dir = ''
        self.__repo = ''

        with open(desc_file, 'r') as pkg_desc:
            pkg_desc_content = load(pkg_desc)

            self.__name = pkg_desc_content['name']
            self.__branch = pkg_desc_content['branch']
            self.__repo = pkg_desc_content['repo']

        self.__dir = '{}/{}/.repo'.format(
            parent_repo,
            pkg_name
        )

    @property
    def name(self):
        """
        Get the name of the package according to the pkg_desc file.

        :returns: The package name.

        """
        return self.__name

    @property
    def repo(self):
        """
        Get the repo url of the package according to the pkg_desc file.

        :returns: The repo url.

        """
        return self.__repo

    @property
    def dir(self):
        """
        Get the package directory.

        :returns: The local package directory.

        """
        return self.__dir

    @property
    def branch(self):
        """
        Get the package branch according to the pkg_desc file.

        :returns: The package branch.

        """
        return self.__branch
