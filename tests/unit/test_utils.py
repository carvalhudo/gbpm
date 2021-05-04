from unittest import TestCase, main

from utils import Utils

class UtilsTest(TestCase):

    """
    Implementation of unit tests for Utils class.

    """

    def test_valid_https_repo_entry(self):
        """
        GIVEN the user specify a valid https repo link.
        WHEN  the user attempts to retrieve the repo ID.
        THEN  the function must return the correct repo ID.

        """
        entry = 'https://github.com/foo/bar.git'

        self.assertEqual(
            Utils.get_repo_id(entry), 'foo/bar'
        )

    def test_valid_ssh_repo_entry(self):
        """
        GIVEN the user specify a valid ssh repo link.
        WHEN  the user attempts to retrieve the repo ID.
        THEN  the function must return the correct repo ID.

        """
        entry = 'git@github.com:bar/foo.git'

        self.assertEqual(
            Utils.get_repo_id(entry), 'bar/foo'
        )

    def test_invalid_https_repo_entry(self):
        """
        GIVEN the user specify a invalid https repo link.
        WHEN  the user attempts to retrieve the repo ID.
        THEN  the function must return an empty string.

        """
        entry = 'https://github.com/foo/bar.get'

        self.assertEqual(
            Utils.get_repo_id(entry), ''
        )

    def test_invalid_ssh_repo_entry(self):
        """
        GIVEN the user specify a invalid ssh repo link.
        WHEN  the user attempts to retrieve the repo ID.
        THEN  the function must return an empty string.

        """
        entry = 'git@github.c:foo/bar.git'

        self.assertEqual(
            Utils.get_repo_id(entry), ''
        )

    def test_random_repo_entry(self):
        """
        GIVEN the user specify a invalid repo link.
        WHEN  the user attempts to retrieve the repo ID.
        THEN  the function must return an empty string.

        """
        entry = 'foo:bar.git'

        self.assertEqual(
            Utils.get_repo_id(entry), ''
        )

if __name__ == "__main__":
    main()
