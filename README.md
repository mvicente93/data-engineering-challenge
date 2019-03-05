
# Data Engineering Challenge

This repo contains a possible solution to [Unbabel's Data Engineering Challenge](https://github.com/Unbabel/data-engineering-challenge)

## Setup

This project was developed and should be run in Python 3.5.2.
For the initial setup, please consider the following instructions

```shell
git clone https://github.com/mvicente93/data-engineering-challenge.git
cd data-engineering-challenge
python3 -m venv venv
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
  --type {sma, ema}, -t {sma, ema}
                        Moving Average algorithm to use (defaults to 'sma')
  --event_name {translation_delivered,translation_requested}, -e {translation_delivered,translation_requested}
                        Which event to process (defaults to
                        'translation_delivered')
  --source_language SOURCE_LANGUAGE
                        Process only translations from given language
  --target_language TARGET_LANGUAGE
                        Process only translations to given language
```

## Objective

The main objetive stated in the problem definition was that to implement a solution that could calculate a moving average delivery time of all events, aggregated by the minute, for a given time frame and write the result to a file. 
From my understanding of Unbabel's challenges, that is, dealing with translation models between different languages where each language has its own specificities and the nature of moving average variations I decided to add the following requirements to the problem:

- The solution should support filtering events according to the source language and target language (or both)
- The solution should be easily extensible to other moving average variations

## Solution 

The main premise of the presented solution was to be able to iterate the existing windows of X minutes in the underlying data and apply a moving average variation to each window. 
To achieve this, irrelevant data, like non-delivery events, has to be filtered out and the remaining must be transformed into per-minute aggregations of event durations and occurences. This aggregation allows the application of a moving average variation of choice, by providing the datapoints existing in each window. Both **SMA** (Simple Moving Average) and **EMA** (Exponential Moving Average) versions were implemented.
To finalize, the result obtained in each window should be written to an output.

## Architecture

The designed architecture is a standard pipeline of reading, transforming and writing data from one format to another. It has a defined separation of concerns and aims for and abstraction layer over the existing windows. It also leverages the ability of the Pandas library read and transform raw data. It can be divided into the following components

### [readers.py](unbabel_cli/readers.py)
Classes aimed specifically at reading a data source and returning a pandas  **DataFrame**. A **JsonReader** and **CsvReader** were implemented.

### [transformers.py](unbabel_cli/transformers.py)
The **DataTransformer** class has the responsibility to apply the supported filters to the **DataFrame** and return the per-minute aggregated version of the data, also represented through a **DataFrame**.

### [iterators.py](unbabel_cli/iterators.py)
The iterator classes consist of custom **DataFrame** iterators that can go over the aggregated data according to the defined window range and generate a **Window** object per iteration.

### [windows.py](unbabel_cli/windows.py)
Window classes are a representation of a time frame. Each one encapsulates the required logic of a specific moving average algorithm.

### [writers.py](unbabel_cli/writers.py)
Writer classes are aimed at writing the developed iterators to a specific output. A **JsonWriter** and **StdoutWriter** writers were implemented.

### [unbabel_cli.py](unbabel_cli.py)
The engined that provides the command-line interface and runs the pipeline.

## TO DO
Comment code
