#!/usr/bin/python3

import sys
from input import InputReader
from api import APIAccess
from output import OutputWriter


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    input_reader = InputReader('txt', 'test.txt')
    words = input_reader.getInput()

    api = APIAccess(words)
    definitions = api.getBatchDictInfo()

    output_writer = OutputWriter('csv', 'test.csv')
    output_writer.writeOutput(definitions)


if __name__ == "__main__":
    main()
