import argparse
import json
import random
import uuid
import sys
from datetime import datetime
from datetime import timedelta


TIMESTAMP_DAY_RANGE = 7
# Give more weight to delivered events
EVENTS = ['translation_delivered'] * 7 + ['translation_requested'] * 3
LANGUAGES = ['en', 'fr', 'pt', 'it', 'es'] 
CLIENTS = ['easyjet', 'ryanair', 'booking', 'unbabel']
MAX_DURATION = 100
MAX_NR_WORDS = 500


def run(n_events, output_file="sample_events.json"):
    
    with open(output_file, 'w') as f:
        events = []
        for _ in range(n_events):
            events.append(generate_event())
        timeseries = map(lambda a: json.dumps(a)+'\n', sorted(events, key=lambda e: e['timestamp']))
        f.writelines(timeseries)

def generate_event():
    event = {}
    event['timestamp'] = generate_random_timestamp()
    event['event_name'] = random.choice(EVENTS)
    event['source_language'] = random.choice(LANGUAGES)
    # Don't allow translations to the same language
    allowed_targets = LANGUAGES.copy()
    allowed_targets.remove(event['source_language'])
    event['target_language'] = random.choice(allowed_targets)
    event['client_name'] = random.choice(CLIENTS)
    event['duration'] = random.randrange(MAX_DURATION)
    event['nr_words'] = random.randrange(MAX_NR_WORDS)
    event['translation_id'] = str(uuid.uuid4().hex)
    return event

def generate_random_timestamp():
    return (datetime.now() - timedelta(days=random.randrange(TIMESTAMP_DAY_RANGE)) * random.random()).strftime('%Y-%m-%d %H:%M:%S.%f')

def generate_cli_parser():
    parser = argparse.ArgumentParser(description='Setup Unbabel CLI')
    parser.add_argument('--n_events', '-n',
                        help='Number of events to generate',
                        type=int,
                        default=1000)
    parser.add_argument('--output_file', '-o',
                        help="Output file name")
    return parser
    
if __name__ == "__main__":
    cli_parser = generate_cli_parser()
    cli_args = cli_parser.parse_args(sys.argv[1:])
    run(cli_args.n_events, cli_args.output_file)