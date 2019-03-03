import sys
import argparse

def run(input_file, window_size, origin_language=None, target_language=None):
    print('Still working on it')

def generate_cli_parser():
    parser = argparse.ArgumentParser(description='Unbabel CLI')
    parser.add_argument('--input_file', '-f',
                        help='File to process',
                        required=True)
    parser.add_argument('--window_size', '-w',
                        help='Window size for moving average in minutes (defaults to 10)',
                        required=True,
                        default=10)
    parser.add_argument('--origin_language',
                        help='Process only translations from given language')
    parser.add_argument('--target_language',
                        help='Process only translations to given language')
    return parser
    
    
if __name__ == "__main__":
    cli_parser = generate_cli_parser()
    cli_args = cli_parser.parse_args(sys.argv[1:])
    run(cli_args.input_file, 
        cli_args.window_size, 
        cli_args.origin_language, 
        cli_args.target_language)