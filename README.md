# Data Engineering Challenge

This repo contains a possible solution to [Unbabel's Data Engineering Challenge](https://github.com/Unbabel/data-engineering-challenge)

## Setup

This project was developed and should be run in Python 3.5.2.
For the initial setup, please consider the following instructions

```shell
git clone https://github.com/mvicente93/data-engineering-challenge.git
cd data-engineering-challenge
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py
```

This will clone the code from this repo, create a [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html) and install the necessary project dependencies (in this case [pandas](https://pandas.pydata.org/)).
The script setup.py generates a default input file 'sample_events.json' containing 1000 events.
This project also includes a test suite, that can be run using
```shell
python -m unittest 
```
### Running

To run a default configuration of the developed unbabel_cli simply run

```shell
python unbabel_cli.py -f sample_events.json
```
This will process the sample_events.json file using a [Simple Moving Average](https://en.wikipedia.org/wiki/Moving_average#Simple_moving_average) and a window of 10 minutes. The results to an output file called 'output.json'

The CLI supports a number of different configuration parameters which are detailed using the -h flag
```shell
python unbabel_cli.py -h

usage: unbabel_cli.py [-h] --file FILE [--output_format {stdout,json}]
                      [--window_size WINDOW_SIZE] [--type {sma}]
                      [--event_name {translation_delivered,translation_requested}]
                      [--source_language SOURCE_LANGUAGE]
                      [--target_language TARGET_LANGUAGE]

Unbabel CLI

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Path to file to process - json and csv files are
                        supported
  --output_format {stdout,json}, -o {stdout,json}
                        Output format (defaults to json)
  --window_size WINDOW_SIZE, -w WINDOW_SIZE
                        Window size for moving average in minutes (defaults to
                        10)
  --type {sma}, -t {sma}
                        Moving Average algorithm to use (defaults to 'sma')
  --event_name {translation_delivered,translation_requested}, -e {translation_delivered,translation_requested}
                        Which event to process (defaults to
                        'translation_delivered')
  --source_language SOURCE_LANGUAGE
                        Process only translations from given language
  --target_language TARGET_LANGUAGE
                        Process only translations to given language
```

## Solution

The main objetive stated in the problem definition was that to implement a solution that could calculate a moving average delivery time of all events, aggregated by the minute, for a given time frame. 
From my understanding of Unbabel's challenges, that is, dealing with translation models between different languages where each language has its own challenges and from my understanding of moving averages and its variations, I decided to add the following requirements to the problem:

- The solution should support filtering events according to the source language and target language (or both)
- The solution should be easily extensible to other moving average variations