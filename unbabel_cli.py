import os
import sys
import argparse
from unbabel_cli.readers import JsonReader
from unbabel_cli.readers import CsvReader
from unbabel_cli.transformers import SMADataTransformer
from unbabel_cli.iterators import SMAWindowIterator
from unbabel_cli.writers import JsonWriter
from unbabel_cli.writers import StdoutWriter


READERS = {
    '.json': JsonReader,
    '.csv': CsvReader
}

TRANSFORMERS = {
    'sma': SMADataTransformer
}

ITERATORS = {
    'sma': SMAWindowIterator
}

WRITERS = {
    'json': JsonWriter,
    'stdout': StdoutWriter
}

EVENT_OPTIONS = ['translation_delivered', 'translation_requested']

def run(input_filename, output_format, window_size, type, event_name, 
        source_language=None, target_language=None):

    input = read_input(input_filename)
    prepared_input = transform_input(input, type, event_name, source_language, target_language)
    iterator = get_iterator(prepared_input, window_size, type)
    write_output(iterator, output_format)

def read_input(filename):
    reader = get_filereader(filename)
    if reader:
        return reader().read(filename)

def get_filereader(filename):
    _, extension = os.path.splitext(filename)
    return READERS.get(extension, None)

def transform_input(input, ma_type, event_name, source_language=None, target_language=None):
    data_transformer = TRANSFORMERS.get(ma_type, None)
    if data_transformer:
        params = get_transformation_parameters(event_name, source_language, target_language)
        return data_transformer(input).transform(params)

def get_transformation_parameters(event_name, source_language, target_language):
    params = [('event_name', event_name)]
    if source_language:
        params.append(('source_language', source_language))
    if target_language:
        params.append(('target_language', target_language))

    return params

def get_iterator(input, window_size, ma_type):
    iterator = ITERATORS.get(ma_type, None)
    if iterator:
        return iterator(input, window_size)

def write_output(iterator, output):
    writer = WRITERS.get(output, None)
    if writer:
        writer().write(iterator)
    
def generate_cli_parser():
    parser = argparse.ArgumentParser(description='Unbabel CLI')
    parser.add_argument('--file', '-f',
                        help='Path to file to process - json and csv files are supported',
                        required=True)
    parser.add_argument('--output_format', '-o',
                        help="Output format (defaults to json)",
                        default="json",
                        choices=WRITERS.keys())
    parser.add_argument('--window_size', '-w',
                        help='Window size for moving average in minutes (defaults to 10)',
                        default=10,
                        type=int)
    parser.add_argument('--type', '-t',
                        help="Moving Average algorithm to use (defaults to 'sma')",
                        default='sma',
                        choices=ITERATORS.keys())
    parser.add_argument('--event_name', '-e',
                        help="Which event to process (defaults to 'translation_delivered')",
                        default='translation_delivered',
                        choices=EVENT_OPTIONS)
    parser.add_argument('--source_language',
                        help='Process only translations from given language')
    parser.add_argument('--target_language',
                        help='Process only translations to given language')
    return parser
    
    
if __name__ == "__main__":
    cli_parser = generate_cli_parser()
    cli_args = cli_parser.parse_args(sys.argv[1:])
    run(cli_args.file,
        cli_args.output_format,
        cli_args.window_size, 
        cli_args.type,
        cli_args.event_name,
        cli_args.source_language, 
        cli_args.target_language)