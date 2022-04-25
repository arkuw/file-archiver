import os
from datetime import datetime
import shutil
from fileinfo import FileInfo, getmd5
from watchdog.events import FileSystemEventHandler
from pathlib import Path


def archive_file(fileinfo:FileInfo, archive_folder='.bak'):
    suffix = datetime.fromtimestamp(fileinfo.modified).strftime(".%Y%m%d_%H%M%S.bak")
    archive_folder = os.path.join(os.path.dirname(fileinfo.path), archive_folder)
    Path(archive_folder).mkdir(parents=True, exist_ok=True)
    backuppath = os.path.join(archive_folder, os.path.basename(fileinfo.path) + suffix)
    if not os.path.exists(backuppath):
        shutil.copyfile(fileinfo.path, backuppath)
    elif getmd5(fileinfo.path) != getmd5(backuppath):
        shutil.copyfile(fileinfo.path, backuppath)

class ArchiveHandler(FileSystemEventHandler):
    fileinfos: dict[str, FileInfo]
    watchpaths: list[str]
    archive_folder: str
    def __init__(self, watchlist: list[str], archive_folder:str ='.bak'):
        self.fileinfos, self.watchpaths = {}, []
        self.archive_folder = archive_folder
        for f in watchlist:
            filepath = os.path.abspath(f)
            assert os.path.exists(filepath)
            if filepath not in self.fileinfos:
                self.fileinfos[filepath] = FileInfo(filepath)
                archive_file(self.fileinfos[filepath], self.archive_folder)
            folderpath = os.path.dirname(filepath)
            if folderpath not in self.watchpaths:
                self.watchpaths.append(folderpath)
    
    def on_modified(self, event):
        filepath = os.path.abspath(event.src_path)
        if filepath in self.fileinfos:
            if self.fileinfos[filepath].update():
                print(filepath + ' changed!!!')
                archive_file(self.fileinfos[filepath], self.archive_folder)
                return True
        return False
