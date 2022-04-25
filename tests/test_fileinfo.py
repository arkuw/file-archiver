from os import remove
import unittest
from fileinfo import *

class TestCase(unittest.TestCase):
    def test1(self):
        filename = 'test.txt' 
        with open(filename, 'w') as f:
            f.write('hello world')
        md5 = getmd5(filename)
        fileinfo = FileInfo('test.txt')
        self.assertTrue(md5 == '5eb63bbbe01eeed093cb22bb8f5acdc3')
        self.assertTrue(fileinfo.md5 == '5eb63bbbe01eeed093cb22bb8f5acdc3')
        self.assertTrue(fileinfo.name == 'test.txt')
        self.assertTrue(fileinfo.size == 11)
        self.assertTrue(fileinfo.lastmd5 is None)
        lastmodified = fileinfo.modified
        with open(filename, 'w') as f:
            f.write('hello world')
        self.assertTrue(not fileinfo.update())
        self.assertTrue(md5 == '5eb63bbbe01eeed093cb22bb8f5acdc3')
        self.assertTrue(fileinfo.md5 == '5eb63bbbe01eeed093cb22bb8f5acdc3')
        self.assertTrue(fileinfo.name == 'test.txt')
        self.assertTrue(fileinfo.size == 11)
        self.assertTrue(fileinfo.lastmd5 is None)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('hello world 你好')
        self.assertTrue(fileinfo.update())
        self.assertTrue(fileinfo.md5 == 'b19dff8249b67fc0a87a3c06eb691bf3')
        self.assertTrue(fileinfo.lastmd5 == '5eb63bbbe01eeed093cb22bb8f5acdc3')
        self.assertTrue(fileinfo.name == 'test.txt')
        self.assertTrue(fileinfo.size == 18)
        if not fileinfo.modified >= lastmodified:
            print(fileinfo.modified)
            print(lastmodified)
        self.assertTrue(fileinfo.modified >= lastmodified)
        remove(filename)


if __name__ == '__main__':
    unittest.main()
