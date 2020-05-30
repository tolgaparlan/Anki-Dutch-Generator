#!/usr/bin/python3

import argparse
import configparser

from api import APIAccess
from audio import Audio
from input import InputReader
from output import OutputWriter


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--quiet', help='Runs the code in silent mode',
                        default=False, action='store_true')
    parser.add_argument('-c', '--config', type=str, metavar='config_file',
                        help='The path for the config file',
                        default='config.ini')
    args = parser.parse_args()

    # Read the config file options
    config = configparser.ConfigParser()
    config.read(args.config)

    # Initialize the classes
    api = APIAccess(config['LANGUAGE']['L2'], config['LANGUAGE']['L1'],
                    config.getboolean('PREFERENCES', 'PreferLongSentences'))
    input_reader = InputReader('txt', config['PATHS']['InputFile'])
    output_writer = OutputWriter('csv', config['PATHS']['OutputFile'])
    audio = Audio(config['LANGUAGE']['L2'], config['PATHS']['AudioFolder'])

    # Read the input file and get all the distinct meanings for each
    # word, then append them to the output file
    failed = []
    for word in input_reader.get_next_word():
        results = api.get_dict_info(word)

        # Try to find the audio file for the word and update the results
        audio_file = audio.get_audio(word)
        for result in results:
            result['Pronounciation'] = audio_file

        output_writer.write_output(results)

        # Book keeping and printing
        if not len(results):
            failed.append(word)

        if not args.quiet:
            print(f'{word} finished with {len(results)} results')

    if not args.quiet:
        print(f'Failed: {failed}')


if __name__ == "__main__":
    main()
