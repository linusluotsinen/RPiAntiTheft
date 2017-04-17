from abc import ABCMeta, abstractmethod

import os
import os.path
import json

class DataStore:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.data = None

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

class FileDataStore(DataStore):
    __metaclass__ = ABCMeta

    def __init__(self, file):
        super(FileDataStore, self).__init__()
        self.file = file
        #if self.is_file() == False:
        #    self.save()

    def get_file(self):
        return self.file

    def is_file(self):
        return os.path.isfile(self.file)

    def file_size(self):
        size = 0
        if self.is_file() == True:
            size = os.stat(self.file).st_size
        return size

class JSONDataStore(FileDataStore):
    def __init__(self, file):
        super(JSONDataStore, self).__init__(file)

    def save(self):
        with open(self.file,'w') as f:
            json.dump(self.get_data(), f)

    def load(self):
        if self.is_file() == True:
            with open(self.file) as f:
                self.set_data(json.load(f))
        
if __name__ == '__main__':
    pass



