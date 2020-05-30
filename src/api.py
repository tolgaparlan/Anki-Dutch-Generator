from os import environ

import requests


# TODO: implement different languages
class APIAccess:
    """Handles the access to the lexicala api"""
    BASE_URL = "https://dictapi.lexicala.com/"

    def __init__(self, input_lang: str, output_lang: str):
        self.session = requests.Session()
        self.input_lang = input_lang
        self.output_lang = output_lang
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
        for meaning in self.__get_search_data(word)['results']:
            entry_data = self.__get_entry_data(meaning['id'])

            # list with all the different senses of this word
            senses = entry_data['senses']
            # headword is the dict with information about the word
            headword = entry_data['headword']
            # sometimes it's an array. just take the first one
            if type(headword) is list:
                headword = headword[0]

            gender = self.__parse_gender(headword)

            sense_objects = self.__parse_sense_objects(senses)
            for el in sense_objects:
                el['Gender'] = gender
                el['Word'] = headword['text'].title()

                # Add 'to' the beginning of the verb translations
                if headword['pos'] == 'verb' and not el['Translation'].startswith('to '):
                    el['Translation'] = "to " + el['Translation']

        return sense_objects

    def __get_search_data(self, word) -> requests.Response:
        return self.session.get(url=self.BASE_URL + 'search',
                                params={'source': 'global',
                                        'language': 'nl',
                                        'text': word}).json()

    def __get_entry_data(self, entry_id):
        return self.session.get(url=self.BASE_URL + 'entries/' + entry_id).json()

    @staticmethod
    def __parse_gender(headword_obj):
        # gender is only applicable to nouns, and common to all senses
        if 'gender' not in headword_obj:
            return ''

        if headword_obj['gender'] == 'neuter':
            return 'Het'
        else:
            return 'De'

    @staticmethod
    def __parse_sense(sense):
        english_translations = sense['translations']['en']
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
        # TODO: get the longest sentence instead?
        # TODO: Scrape better here
        try:
            example_sentences = sense["examples"][0]["text"]
        except Exception:
            example_sentences = ""

        return {'Translation': english_translations.title(),
                'Text': example_sentences,
                'Definition': definition}

    def __parse_sense_objects(self, senses):
        sense_objects = []
        # Go over every sense and parse them
        for sense in senses:
            # some senses don't have translations
            if "translations" not in sense:
                continue

            output = self.__parse_sense(sense)
            sense_objects.append(output)

        return sense_objects
