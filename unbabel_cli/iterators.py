from abc import ABC
from abc import abstractclassmethod
from unbabel_cli.transformers import SMADataTransformer
from unbabel_cli.windows import SMAWindow


class AbstractWindowIterator(ABC):

    def __init__(self, data, window_size):
        self.left_index = 0
        self.right_index = 1
        self.data = data
        self.window_size = window_size
        self.window = None
        super().__init__()

    def next(self):    
        while True:
            window = self._next_window()
            if window:
                yield window
            else:
                break

    def _update_window_indexes(self):
        if self.right_index < self.window_size:
            self.right_index += 1
        else:
            self.right_index += 1
            self.left_index += 1

    @abstractclassmethod
    def _next_window(self):
        pass


class SMAWindowIterator(AbstractWindowIterator):
    
    def _next_window(self):

        if self.right_index > len(self.data):
            return

        if self.right_index < self.window_size:
            window = self.data[:self.right_index]
        else:
            window = self.data[self.left_index:self.right_index]
        
        if window.empty:
            return

        self._update_window_indexes()

        return SMAWindow(window)
