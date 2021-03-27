from unittest import TestCase, main

from app.validators import add_repo_validator

class ValidatorsTest(TestCase):

    """
    Implementation of unit tests for validators file

    """

    def valid_https_repo_entry_test(self):
        """
        GIVEN the user used the '-a' option.
        WHEN  the user specify a valid https repository.
        THEN  the validator must return true.
        """
        entry = 'master:https://github.com/foo/bar.git'

        self.assertTrue(add_repo_validator(entry))

    def valid_ssh_repo_entry_test(self):
        """
        GIVEN the user used the '-a' option.
        WHEN  the user specify a valid ssh repository.
        THEN  the validator must return true.
        """
        entry = 'master:git@github.com:foo/bar.git'

        self.assertTrue(add_repo_validator(entry))

    def valid_https_repo_without_branch_entry_test(self):
        """
        GIVEN the user used the '-a' option.
        WHEN  the user specify a valid https repository without a branch.
        THEN  the validator must return false.
        """
        entry = 'https://github.com/foo/bar.git'

        self.assertFalse(add_repo_validator(entry))

    def valid_https_repo_with_empty_branch_entry_test(self):
        """
        GIVEN the user used the '-a' option.
        WHEN  the user specify a valid https repository with an empty branch.
        THEN  the validator must return false.
        """
        entry = ':https://github.com/foo/bar.git'

        self.assertFalse(add_repo_validator(entry))

    def valid_ssh_repo_without_branch_entry_test(self):
        """
        GIVEN the user used the '-a' option.
        WHEN  the user specify a valid ssh repository without a branch.
        THEN  the validator must return false.
        """
        entry = 'git@github.com:foo/bar.git'

        self.assertFalse(add_repo_validator(entry))

    def valid_ssh_repo_with_empty_branch_entry_test(self):
        """
        GIVEN the user used the '-a' option.
        WHEN  the user specify a valid ssh repository with an empty branch.
        THEN  the validator must return false.
        """
        entry = ':git@github.com:foo/bar.git'

        self.assertFalse(add_repo_validator(entry))

    def invalid_https_repo_entry_test(self):
        """
        GIVEN the user used the '-a' option.
        WHEN  the user specify an invalid https repository.
        THEN  the validator must return false.
        """
        entry = 'master:https://github.com/foo/bar.get'

        self.assertFalse(add_repo_validator(entry))

    def invalid_ssh_repo_entry_test(self):
        """
        GIVEN the user used the '-a' option.
        WHEN  the user specify an invalid ssh repository.
        THEN  the validator must return false.
        """
        entry = 'master:git@github.c:foo/bar.git'

        self.assertFalse(add_repo_validator(entry))

    def random_repo_entry_test(self):
        """
        GIVEN the user used the '-a' option.
        WHEN  the user specify random repository name.
        THEN  the validator must return false.
        """
        entry = 'foo:bar.git'

        self.assertFalse(add_repo_validator(entry))

if __name__ == "__main__":
    main()
