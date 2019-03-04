from unittest import TestCase
from unbabel_cli.readers import JsonReader
from unbabel_cli.transformers import SMADataTransformer
import json
import os


INPUT_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/example_input.json'


class TestSMATransformer(TestCase):
    
    def setUp(self):
        self.sample_input = JsonReader().read(INPUT_FILE_PATH)
    
    def test_transform(self):
        EXPECTED_LEN = 13
        EXPECTED_HEADERS = [('duration', 'events_count'), ('duration', 'duration_sum')]
        EXPECTED_DURATION = 105
        EXPECTED_COUNTS = 3

        prepared_data = SMADataTransformer(self.sample_input).transform()
        self.assertEqual(len(prepared_data), EXPECTED_LEN)
        self.assertEqual(list(prepared_data), EXPECTED_HEADERS)
        self.assertEqual(prepared_data.duration.duration_sum.sum(), EXPECTED_DURATION)
        self.assertEqual(prepared_data.duration.events_count.sum(), EXPECTED_COUNTS)

    def test_transform_with_filter(self):
        EXPECTED_LEN = 9
        EXPECTED_HEADERS = [('duration', 'events_count'), ('duration', 'duration_sum')]
        EXPECTED_DURATION = 85
        EXPECTED_COUNTS = 2

        prepared_data = SMADataTransformer(self.sample_input).transform([('event_name', 'translation_delivered')])
        self.assertEqual(len(prepared_data), EXPECTED_LEN)
        self.assertEqual(list(prepared_data), EXPECTED_HEADERS)
        self.assertEqual(prepared_data.duration.duration_sum.sum(), EXPECTED_DURATION)
        self.assertEqual(prepared_data.duration.events_count.sum(), EXPECTED_COUNTS)
