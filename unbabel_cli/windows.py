from abc import ABC
from abc import abstractclassmethod
from datetime import timedelta

class AbstractWindow(ABC):

    TIMESTAMP_STRING = 'date'
    FORMAT_SPEC = '.3f'

    def __init__(self, df):
        self.window = df
        self.timestamp = self.get_timestamp()
        self.mean = self.get_mean()        
        super().__init__()

    @abstractclassmethod
    def get_mean(self):
        pass

    @abstractclassmethod
    def get_timestamp(self):
        pass
    
    def __dict__(self, event_name="event"):
        return {self.TIMESTAMP_STRING: self.timestamp.isoformat(), event_name : format(self.mean, self.FORMAT_SPEC)}


class SMAWindow(AbstractWindow):

    def get_timestamp(self):
        return self.window.index[-1] + timedelta(minutes=1)

    def get_mean(self):
        counts = self.window.duration.events_count.sum()
        return self.window.duration.duration_sum.sum() / counts if counts else 0
