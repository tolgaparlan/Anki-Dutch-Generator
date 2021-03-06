from os import environ

import requests


# TODO: implement different languages
class APIAccess:
    """Handles the access to the lexicala api"""
    BASE_URL = "https://dictapi.lexicala.com/"

    def __init__(self, input_lang: str, output_lang: str,
                 prefer_long_examples: bool, cloze: bool):
        self.session = requests.Session()
        self.input_lang = input_lang
        self.output_lang = output_lang
        self.prefer_long_examples = prefer_long_examples
        self.cloze = cloze
        self.session.auth = (
            environ['LEXICALA_USER'], environ['LEXICALA_PASS'])

    def get_dict_info(self, word: str) -> list:
        """
        Gets online info for a word
        :param word: The word to search
        :return: A list with object filled with info about each sense of the word
        """
        # Get different meanings for the word
        # and go over every single dictionary entry
        sense_objects = []
        for entry_data in self.__get_entry_data(word):
            # list with all the different senses of this word
            senses = entry_data['senses']
            # headword is the dict with information about the word
            headword = entry_data['headword']
            # sometimes it'sentence an array. just take the first one
            if type(headword) is list:
                headword = headword[0]

            gender = self.__parse_gender(headword)

            sense_objects = self.__parse_sense_objects(headword, senses)
            for el in sense_objects:
                el['Gender'] = gender
                el['Word'] = headword['text'].title()

                # Add 'to' the beginning of the verb translations
                if headword['pos'] == 'verb' and not el['Translation'].startswith('to '):
                    el['Translation'] = "to " + el['Translation']

        return sense_objects

    def __get_entry_data(self, word: str) -> list:
        """
        Retrieves info about every sense of the word and returns the
        sense objects in a list.
        :param word: The L2 word to search for
        :return: A list of entries (https://dictapi.lexicala.com/swagger-docs/#/data/get_entry)
        """
        r = self.session.get(url=self.BASE_URL + 'search',
                             params={'source': 'global',
                                     'language': 'nl',
                                     'text': word})

        if not r.ok:
            raise PermissionError('Problem with API connection: ' + r.json()['message'])

        entries = []
        for meaning in r.json()['results']:
            r2 = self.session.get(url=self.BASE_URL + 'entries/' + meaning['id'])

            if not r2.ok:
                raise PermissionError('Problem with API connection: ' + r2.json()['message'])

            entries.append(r2.json())
        return entries

    @staticmethod
    def __parse_gender(headword_obj):
        # gender is only applicable to nouns, and common to all senses
        if 'gender' not in headword_obj:
            return ''

        if headword_obj['gender'] == 'neuter':
            return 'Het'
        else:
            return 'De'

    def __parse_sense(self, headword: dict, sense: dict):
        english_translations = sense['translations']['en']

        definition = ''
        if 'definition' in sense:
            definition = sense['definition']

        # Get all the english translations for the sense
        # Translations might be an array with dicts or a single dict
        if type(english_translations) is list:
            english_translations = ', '.join(
                [el['text'] for el in english_translations])
        elif type(english_translations) is dict:
            english_translations = english_translations['text']
        else:
            raise Exception(
                "Translation format unexpected:\n" + str(sense))

        # If there are any, get the first example sentence
        # TODO: Scrape better here
        try:
            example_sentence = self.__pick_example(sense["examples"])
        except Exception:
            example_sentence = ""

        return {
            'Translation': english_translations.title(),
            'Text': self.__attempt_cloze(headword, example_sentence),
            'Definition': definition
        }

    def __attempt_cloze(self, headword: dict, sentence: str) -> str:
        """
        Attempts to match the word in the sentence and turn the sentence into
        the cloze format. Will not work in situations where any inflection
        don't exactly match the used format of the word in the sentence.
        TODO: Try to improve this. Especially for composite words
        :param headword: contains information about the dictionary entry
        :param sentence: the example sentence containing a version of the word
        """

        if not self.cloze:
            return sentence

        # gathers all the inflections of the word
        all_versions = [headword['text']]

        if 'inflections' in headword:
            all_versions += [el['text'].replace('|', '') for el in
                             headword['inflections']]

        sentence_split = sentence.split(' ')
        for idx, word in enumerate(sentence_split):
            if word.strip(',.!?:()\'').lower() in all_versions:
                word = '{{c1::' + word + '}}'

            sentence_split[idx] = word

        return ' '.join(sentence_split)

    def __pick_example(self, examples: list) -> str:
        """
        Picks the longest or shortest example from the bunch, depending which
        one is preferred
        :param examples: a list of examples for the sense as fetched from API
        :return: The longest/shortest example sentence
        """
        picked = examples[0]["text"]
        if len(examples) == 0:
            return picked

        for example in examples:
            if (len(example["text"]) > len(
                    picked)) == self.prefer_long_examples:
                picked = example["text"]

        return picked

    def __parse_sense_objects(self, headword: dict, senses: list):
        sense_objects = []
        # Go over every sense and parse them
        for sense in senses:
            # some senses don't have translations
            if "translations" not in sense:
                continue

            output = self.__parse_sense(headword, sense)
            sense_objects.append(output)

        return sense_objects
