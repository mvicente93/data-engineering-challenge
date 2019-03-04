import json
from abc import ABC
from abc import abstractclassmethod


class AbstractWriter(ABC):
    @abstractclassmethod
    def write(self, iterator):
        pass

class JsonWriter(AbstractWriter):
    def write(self, iterator, output='output.json'):
        f = open(output, 'w')
        entry_list = []
        for entry in iterator.next():
            entry_list.append(json.dumps(entry.__dict__()) + '\n')
        f.writelines(entry_list)
        f.close()

class StdoutWriter(AbstractWriter):
    def write(self, iterator):
        for entry in iterator.next():
            print(entry.__dict__())