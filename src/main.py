#!/usr/bin/python3

import argparse
import configparser

from api import APIAccess
from audiomanager import AudioManager
from input import InputReader
from output import OutputWriter


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', type=str, metavar='config_file',
                        help='The path for the config file',
                        default='config.ini')
    args = parser.parse_args()

    # Read the config file options
    config = configparser.ConfigParser()
    config.read(args.config)

    # Initialize the classes
    api = APIAccess(config['LANGUAGE']['L2'],
                    config['LANGUAGE']['L1'],
                    config.getboolean('EXAMPLE_SENTENCES', 'PreferLongSentences'),
                    config.getboolean('EXAMPLE_SENTENCES', 'Cloze'))
    input_reader = InputReader(config['INPUT']['Mode'],
                               config['INPUT']['FileName'])
    output_writer = OutputWriter(config['OUTPUT'])
    audio = AudioManager(config['LANGUAGE']['L2'],
                         config['AUDIO']['Folder'],
                         config.getboolean('AUDIO', 'Normalize'))

    # Read the input file and get all the distinct meanings for each
    # word, then append them to the output file
    failed = []
    for word in input_reader.get_next_word():
        try:
            results = api.get_dict_info(word)

            # Try to find the audio file for the word and update the results
            audio_file = audio.get_audio(word)
            for result in results:
                result['Pronounciation'] = audio_file

            output_writer.write_output(results)
        except PermissionError as e:
            # Happens if the Lexicala API doesn't allow connection
            print(e)
            print('Terminating the Program')
            exit(0)
        except Exception as e:
            # Shouldn't happen normally
            raise e

        # Book keeping and printing
        if not len(results):
            failed.append(word)

        print(f'{word} finished with {len(results)} results')

    print(f'Failed: {failed}')


if __name__ == "__main__":
    main()
