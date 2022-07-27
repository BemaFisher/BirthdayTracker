import os
import time


class FileWatcher:
    def __init__(self, path, callback):
        """
        Init a new file watcher
        """
        self.path = path
        self.callback = callback
        self.modifiedOn = os.path.getmtime(path)

    def start(self):
        """
        Starts watching a file
        """
        while True:
            time.sleep(0.5)
            modified = os.path.getmtime(self.path)
            if modified != self.modifiedOn:
                self.modifiedOn = modified
                if self.callback():
                    break
