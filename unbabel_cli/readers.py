from abc import ABC
from abc import abstractmethod
import pandas as pd


class FileReader(ABC):

    @abstractmethod
    def read(self, parameter_list):
        raise NotImplementedError


class JsonReader(FileReader):
    def read(self, input_file):
        return pd.read_json(input_file, lines=True)


class CsvReader(FileReader):
    def read(self, input_file):
        return pd.read_csv(input_file)