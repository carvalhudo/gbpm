
class MirrorsMgr:

    """
    Class responsible for the management of the mirrors file of gbpm

    The mirrors file contains a list of package repositories which will
    be used during the 'update' operation. Such file has the same goal
    of 'sources.list' of 'apt' package manager
    """

    mirrors_file = '/etc/gbpm/mirrors.csv'
    #mirrors_file = '../mirrors.csv'

    @classmethod
    def get_mirrors(cls):
        """
        Get the mirrors file content
        :returns: The mirrors file content

        """
        with open(cls.mirrors_file, 'r') as mirrors:
            return [
                mirror.replace('\n', '') for mirror in mirrors.readlines()
            ]
