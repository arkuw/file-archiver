import unittest
from fileinfo import *
from archivehandler import ArchiveHandler
from datetime import datetime
from time import sleep
from pathlib import Path
import shutil

class event: pass

class TestCase(unittest.TestCase):
    def test1(self):
        Path("f1").mkdir(parents=True, exist_ok=True)
        Path("f2").mkdir(parents=True, exist_ok=True)
        filename = 'f1/test1.txt'
        filename2 = 'f2/test1.txt'
        with open(filename, 'w') as f:
            f.write('hello world')
        with open(filename2, 'w') as f:
            f.write('hello world')
        
        watchlist = [filename, filename2]
        handler = ArchiveHandler(watchlist)
        
        self.assertTrue('f1' in str(handler.watchpaths))
        self.assertTrue('f2' in str(handler.watchpaths))
        
        # fileinfo = next(iter(handler.fileinfos))
        suffix = datetime.fromtimestamp(os.path.getmtime(filename)).strftime(".%Y%m%d_%H%M%S.bak")
        self.assertTrue(os.path.join(os.path.dirname(os.path.abspath(filename + suffix)), handler.archive_folder, os.path.dirname(os.path.basename(filename + suffix))))
        event.src_path = next(iter(handler.fileinfos))
        # print(event.src_path)
        # handler.on_modified(event)
        sleep(1) # 1s to make archive file name differ
        with open(filename, 'w') as f:
            f.write('hello world')
        self.assertTrue(not handler.on_modified(event))
        suffix = datetime.fromtimestamp(os.path.getmtime(filename)).strftime(".%Y%m%d_%H%M%S.bak")
        self.assertTrue(not os.path.exists(filename + suffix))
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('hello world 你好')
        self.assertTrue(handler.on_modified(event))
        self.assertTrue(handler.fileinfos[event.src_path].md5 == 'b19dff8249b67fc0a87a3c06eb691bf3')
        self.assertTrue(handler.fileinfos[event.src_path].lastmd5 == '5eb63bbbe01eeed093cb22bb8f5acdc3')
        suffix = datetime.fromtimestamp(os.path.getmtime(filename)).strftime(".%Y%m%d_%H%M%S.bak")
        self.assertTrue(os.path.join(os.path.dirname(os.path.abspath(filename + suffix)), handler.archive_folder, os.path.dirname(os.path.basename(filename + suffix))))
        
        # clean up
        shutil.rmtree('f1')
        shutil.rmtree('f2')
        # remove(filename)
        # for _ in os.listdir('.'):
        #     if _.endswith('.bak'):
        #         remove(_)

if __name__ == '__main__':
    unittest.main()
