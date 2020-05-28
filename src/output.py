import csv


class OutputWriter:
    """Handles writing the output"""

    FIELD_NAMES = ['Word', 'Translation', 'Pronounciation',
                   'Picture', 'Definition', 'Gender', 'Text']

    def __init__(self, mode, filename):
        self.filename = filename
        self.mode = mode

        self.__createOutputFile()

    # Returns the input in a list, each element being a word
    def writeOutput(self, definitions):
        if self.mode == 'csv':
            return self.__writeCsvOutput(definitions)
        else:
            raise Exception("Unrecognized Mode")

    def __writeCsvOutput(self, definitions):
        with open(self.filename, "a") as csv_file:
            w = csv.DictWriter(csv_file, delimiter='\t',
                               fieldnames=self.FIELD_NAMES)
            for line in definitions:
                w.writerow(line)

    # Creates the output file with the given name.
    # Will overwrite any existing files with that name
    def __createOutputFile(self):
        open(self.filename, 'w').close()
