
class MirrorsMgr:

    """
    Implementation of the class responsible for the management of the mirrors
    file of gbpm.

    """

    mirrors_file = '/etc/gbpm/mirrors.csv'

    @classmethod
    def get_mirrors(cls):
        """
        Get the mirrors file content.

        :returns: A list of mirrors.

        """
        with open(cls.mirrors_file, 'r') as mirrors:
            return [
                mirror.replace('\n', '') for mirror in mirrors.readlines()
            ]
