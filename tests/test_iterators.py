from unittest import TestCase
from unbabel_cli.readers import JsonReader
from unbabel_cli.transformers import DataTransformer
from unbabel_cli.iterators import AbstractWindowIterator
from unbabel_cli.iterators import SMAWindowIterator
from unbabel_cli.windows import SMAWindow
import json
import os


INPUT_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/example_input.json'


class TestSMAIterator(TestCase):
    
    def setUp(self):
        self.sample_input = JsonReader().read(INPUT_FILE_PATH)
        self.iterator = SMAWindowIterator(DataTransformer(self.sample_input).transform(), 2)

    def test_index_update_under_window_size(self):
        iterator = SMAWindowIterator("", 2)
        iterator._update_window_indexes()
        self.assertEqual(iterator.left_index, 0)
        self.assertEqual(iterator.right_index, 2)

    def test_index_update_over_window_size(self):
        iterator = SMAWindowIterator("", 1)
        iterator._update_window_indexes()
        self.assertEqual(iterator.left_index, 1)
        self.assertEqual(iterator.right_index, 2)

    def test_next_window(self):
        next = self.iterator._next_window()
        self.assertTrue(isinstance(next, SMAWindow))
