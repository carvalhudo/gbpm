from unittest import TestCase, main
from os import remove

from mirrors_mgr import MirrorsMgr

class MirrorsMgrTest(TestCase):

    """
    Implementation of unit tests for MirrorsMgr class

    """

    def tearDown(self):
        remove(MirrorsMgr.mirrors_file)

    def test_get_multiple_mirrors(self):
        """
        GIVEN the mirrors file contain multiple entries.
        WHEN  the user attempt to retrieve the file content.
        THEN  the call must return a list containing the registered
              mirrors.
        """
        mirrors = [
            'master,https://github.com/user/repo_1.git',
            'master,https://github.com/user/repo_2.git',
            'master,https://github.com/user/repo_3.git',
            'master,https://github.com/user/repo_4.git',
        ]

        with open(MirrorsMgr.mirrors_file, 'w') as mirrors_file:
            for i in mirrors:
                mirrors_file.write(i + '\n')

        content = MirrorsMgr.get_mirrors()

        self.assertEqual(len(mirrors), len(content))
        self.assertEqual(mirrors, content)

    def test_get_single_mirror(self):
        """
        GIVEN the mirrors file contain a single entry.
        WHEN  the user attempt to retrieve the file content.
        THEN  the call must return a list containing only one registered
              mirror.
        """
        mirror = ['master,https://github.com/user/repo.git']

        with open(MirrorsMgr.mirrors_file, 'w') as mirrors_file:
            mirrors_file.writelines(mirror)

        content = MirrorsMgr.get_mirrors()

        self.assertEqual(len(content), len(mirror))
        self.assertEqual(mirror, content)

    def test_get_mirror_from_empty_file(self):
        """
        GIVEN the mirrors file is empty.
        WHEN  the user attempt to retrieve the file content.
        THEN  the call must return an empty list.
        """
        with open(MirrorsMgr.mirrors_file, 'w') as mirrors_file:
            mirrors_file.write('')

        content = MirrorsMgr.get_mirrors()

        self.assertEqual(len(content), 0)

if __name__ == "__main__":
    main()
