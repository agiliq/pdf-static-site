import os
import unittest


class TestCountImagesMarkdown(unittest.TestCase):

    def setUp(self):
        self.img_path = 'linux_images'
        self.md_path = 'linux_md'
        if os.path.isdir(self.img_path):
            self.number_of_images = len(os.listdir(self.img_path))
        if os.path.isdir(self.md_path):
            self.number_of_md_files = len(os.listdir(self.md_path))
            os.system("pelican {0}".format(self.md_path))
        if os.path.isdir('output'):
            self.number_of_files = len(
                [f for f in os.listdir('output') if 'linux-' in f])

    def test_images_equalto_markdownfiles(self):
        self.assertEqual(self.number_of_images, self.number_of_md_files)

    def test_markdownfiles_equalto_htmlfiles(self):
        self.assertEqual(self.number_of_md_files, self.number_of_files)

if __name__ == '__main__':
    unittest.main()
