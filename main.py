import time
from watchdog.observers import Observer
from archivehandler import ArchiveHandler

watchlist = []

with open('watchlist.txt', 'r') as f:
    watchlist = f.read().splitlines() 

event_handler = ArchiveHandler(watchlist)
observer = Observer()
for p in event_handler.watchpaths:
    observer.schedule(event_handler, p, recursive=True)
observer.start()
print('observing ' + str(event_handler.watchpaths))

try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()
