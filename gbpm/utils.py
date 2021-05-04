from re import search

class Utils:

    """
    Implementation of the utils class, which contains a set of utilitary methods.

    """

    @staticmethod
    def get_repo_id(repo_url):
        """
        Get a repository ID.

        :repo_url: Url of the repository.
        :returns: The repository ID (in user/repo_name format).

        """
        pattern_list = [
            'https://(.+?).com/(.+?)/(.+?).git',
            'git@(.+?).com:(.+?)/(.+?).git'
        ]

        for pattern in pattern_list:
            found = search(pattern, repo_url)

            if found:
                return '{}/{}'.format(found.group(2), found.group(3))

        return ''
