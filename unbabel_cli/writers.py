import json
from abc import ABC
from abc import abstractclassmethod


class AbstractWriter(ABC):
    @abstractclassmethod
    def write(self, iterator):
        pass

class JsonWriter(AbstractWriter):
    def write(self, iterator, output='output.json'):
        with open(output, 'w') as f:
            for entry in iterator.next():
                f.write(json.dumps(entry.__dict__()) + '\n')

class StdoutWriter(AbstractWriter):
    def write(self, iterator):
        for entry in iterator.next():
            print(entry.__dict__())