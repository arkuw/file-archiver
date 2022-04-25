import os
import hashlib


def getmd5(path, size=65536):
    m = hashlib.md5()
    with open(path, 'rb') as f:
        b = f.read(size)
        while len(b) > 0:
            m.update(b)
            b = f.read(size)
    return m.hexdigest()

class FileInfo:
    def __init__(self, filepath):
        self.name = os.path.basename(filepath)
        self.path = filepath
        self.md5 = None
        self.update()
    
    def update(self):
        md5 = getmd5(self.path)
        if md5 == self.md5:
            # print('file unchanged!')
            return False
        self.lastmd5 = self.md5
        self.modified = os.path.getmtime(self.path)
        self.size = os.path.getsize(self.path)
        self.md5 = md5
        return True
    
    def __str__(self) -> str:
        return str(self.__dict__)
    