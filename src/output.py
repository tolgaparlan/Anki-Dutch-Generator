import csv


class OutputWriter:
    """Handles writing the output"""

    FIELD_NAMES = ['Word', 'Translation', 'Pronounciation',
                   'Picture', 'Definition', 'Gender', 'Text']

    def __init__(self, mode: str, filename: str):
        self.filename = filename
        self.mode = mode

        self.__create_output_file()

    def write_output(self, definitions):
        if self.mode == 'csv':
            return self.__write_csv_output(definitions)
        else:
            raise Exception("Unrecognized Mode")

    def __write_csv_output(self, definitions):
        with open(self.filename, "a") as csv_file:
            w = csv.DictWriter(csv_file, delimiter='\t',
                               fieldnames=self.FIELD_NAMES)
            for line in definitions:
                w.writerow(line)

    # Creates the output file with the given name.
    # Will overwrite any existing files with that name
    def __create_output_file(self):
        open(self.filename, 'w').close()
