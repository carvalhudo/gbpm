from re import search

class Utils:

    """Docstring for Utils. """

    @staticmethod
    def get_repo_name(repo_url):
        """TODO: Docstring for get_repo_name.

        :repo_url: TODO
        :returns: TODO

        """
        pattern_list = [
            'https://(.+?).com/(.+?)/(.+?).git',
            'git@(.+?).com:(.+?)/(.+?).git'
        ]

        for pattern in pattern_list:
            found = search(pattern, repo_url)

            if found:
                #return '{}/{}'.format(found.group(2), found.group(3))
                return found.group(3)

        return ''
