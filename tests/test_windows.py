from unittest import TestCase
from unbabel_cli.readers import JsonReader
from unbabel_cli.transformers import SMADataTransformer
from unbabel_cli.iterators import AbstractWindowIterator
from unbabel_cli.iterators import SMAWindowIterator
from unbabel_cli.windows import SMAWindow
import json
import os


INPUT_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/example_input.json'


class TestSMAWindows(TestCase):
    
    def setUp(self):
        self.sample_input = JsonReader().read(INPUT_FILE_PATH)
        self.iterator = SMAWindowIterator(SMADataTransformer(self.sample_input).transform(), 2)

    def test_sma_timestamp(self):
        EXPECTED_TS = '2018-12-26T18:12:00'
        window = self.iterator._next_window()
        self.assertEqual(window.get_timestamp().isoformat(), EXPECTED_TS)

    def test_sma_mean(self):
        EXPECTED_MEAN = 20
        window = self.iterator._next_window()
        self.assertEqual(window.get_mean(), EXPECTED_MEAN)
