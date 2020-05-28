#!/usr/bin/python3

import sys
import argparse
from input import InputReader
from api import APIAccess
from output import OutputWriter


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Anki friendly output from about inputted words")

    parser.add_argument('dest', type=str, metavar='input_file',
                        help='The path to the input file')
    parser.add_argument('targ', type=str, metavar='output_file',
                        help='The path to the output file')
    parser.add_argument('input_lang', type=str,
                        help='The language code of the input words')
    parser.add_argument('output_lang', type=str,
                        help='The language code to get the translations in')
    parser.add_argument('-q', '--quiet', help='Runs in silent mode',
                        default=False, action='store_true')
    args = parser.parse_args()

    api = APIAccess(args.input_lang, args.output_lang)
    input_reader = InputReader('txt', 'test.txt')
    output_writer = OutputWriter('csv', 'test.csv')

    # Read the input file and get all the distinct meanings for each
    # word, then append them to the output file
    failed = []
    for word in input_reader.getLine():
        results = api.getDictInfo(word)
        if not len(results):
            failed.append(word)
        output_writer.writeOutput(results)

        if not args.quiet:
            print(f'{word} finished with {len(results)} results')

    if not args.quiet:
        print(f'Failed: {failed}')


if __name__ == "__main__":
    main()
