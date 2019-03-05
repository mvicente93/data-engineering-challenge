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

    @abstractclassmethod
    def get_mean(self):
        pass

    @abstractclassmethod
    def get_timestamp(self):
        pass
    
    def __dict__(self, event_name="average_delivery_time"):
        return {self.TIMESTAMP_STRING: self.timestamp.isoformat(), event_name : format(self.mean, self.FORMAT_SPEC)}


class SMAWindow(AbstractWindow):

    def get_timestamp(self):
        return self.window.index[-1] + timedelta(minutes=1)

    def get_mean(self):
        counts = self.window.duration.events_count.sum()
        return self.window.duration.duration_sum.sum() / counts if counts else 0


class EMAWindow(AbstractWindow):

    def __init__(self, df, last_ema=None):
        self.window = df
        self.last_ema = last_ema
        self.decay = 2 / float((len(df) + 1))
        self.timestamp = self.get_timestamp()
        self.mean = self.get_mean()  

    def get_timestamp(self):
        return self.window.index[-1] + timedelta(minutes=1)

    def get_mean(self):
        counts = self.window.duration.events_count.sum()
        mean = self.window.duration.duration_sum.sum() / counts if counts else 0
        if self.last_ema:
            return (1-self.decay) * self.last_ema + self.decay * mean
        return mean