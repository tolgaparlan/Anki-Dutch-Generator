import csv
import requests


class OutputWriter:
    """Handles writing the output"""

    FIELD_NAMES = ['Word', 'Translation', 'Pronounciation',
                   'Picture', 'Definition', 'Gender', 'Text']

    def __init__(self, config):
        """
        :param config: {Mode, DeckName, ModelName} for ankiconnect, {Mode, Filename} for csv
        """
        print(config['Mode'])
        self.mode = config['Mode']
        if self.mode.endswith('.csv'):
            self.filename = config['Filename']
            self.__create_output_file()
        elif self.mode == 'ankiconnect':
            self.deck_name = config['DeckName']
            self.model_name = config['ModelName']
        else:
            raise Exception('Wrong output mode')

    def write_output(self, definitions: list):
        if self.mode == 'csv':
            self.__output_csv(definitions)
        elif self.mode == 'ankiconnect':
            self.__output_ankiconnect(definitions)

    def __output_ankiconnect(self, definitions):
        for definition in definitions:
            r = requests.post('http://127.0.0.1:8765', json={
                "action": "addNote",
                "version": 6,
                "params": {
                    "note": {
                        "deckName": self.deck_name,
                        "modelName": self.model_name,
                        "fields": definition,
                        "options": {
                            "allowDuplicate": True,
                            "duplicateScope": "deck"
                        },
                    }
                }
            })

        if not r.ok or r.json()['error']:
            raise Exception('AnkiConnect Problem:' + str(r.json()))

    def __output_csv(self, definitions: list):
        """
        Appends the definitions in the list line by line to the csv file
        """
        with open(self.filename, "a") as csv_file:
            w = csv.DictWriter(csv_file, delimiter='\t',
                               fieldnames=self.FIELD_NAMES)
            for line in definitions:
                w.writerow(line)

    def __create_output_file(self):
        """
        Creates the output file.
        Will overwrite any existing files with that name.
        """
        open(self.filename, 'w').close()
