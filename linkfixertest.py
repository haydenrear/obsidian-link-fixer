import unittest
import link_fix
import os
import link_builder


class MyTestCase(unittest.TestCase):
    def test_something(self):
        fixer = link_fix.LinkFixer()
        os.chdir('../')
        fixer.get_file_index(os.curdir)
        fixer.print_missing()
        builder = link_builder.LinkBuilder(fixer.file_indices, fixer.file_manager)
        builder.get_true_links()
        print('\n\n NOT MISSING \n\n')



if __name__ == '__main__':
    unittest.main()
