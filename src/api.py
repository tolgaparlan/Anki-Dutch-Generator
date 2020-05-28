from requests import Session
from os import environ


class APIAccess():
    """Handles the access to the lexicala api"""
    BASE_URL = "https://dictapi.lexicala.com/"

    # TODO: implement different languages
    def __init__(self, input_lang, output_lang):
        self.session = Session()
        self.session.auth = (
            environ['LEXICALA_USER'], environ['LEXICALA_PASS'])

    # Gets online info for a word
    def getDictInfo(self, word):
        # Get different meanings for the word
        # and go over every single dictionary entry
        senseObjects = []
        for meaning in self.__getSearchData(word)['results']:
            entryData = self.__getEntryData(meaning['id'])

            # list with all the different senses of this word
            senses = entryData['senses']
            # headword = information about the word
            headword = entryData['headword']

            gender = self.__parseGender(headword)

            senseObjects = self.__parseSenseObjects(senses)
            for el in senseObjects:
                el['Gender'] = gender
                el['Word'] = headword['text'].title()

        return senseObjects

    def __getSearchData(self, word):
        PARAMS = {'source': 'global',
                  'language': 'nl',
                  'text': word}

        return self.session.get(url=self.BASE_URL + 'search',
                                params=PARAMS).json()

    def __getEntryData(self, id):
        return self.session.get(url=self.BASE_URL + 'entries/' + id).json()

    def __parseGender(self, headwordObj):
        # gender is only applicable to nouns, and common to all senses
        if 'gender' not in headwordObj:
            return ''

        if headwordObj['gender'] == 'neuter':
            return 'Het'
        else:
            return 'De'

    def __parseSense(self, sense):
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
        try:
            example_sentences = sense["examples"][0]["text"]
        except Exception:
            example_sentences = ""

        return {'Translation': english_translations.title(),
                'Text': example_sentences,
                'Definition': definition}

    def __parseSenseObjects(self, senses):
        senseObjects = []
        # Go over every sense and parse them
        for sense in senses:
            # some sense don't have translations
            if "translations" not in sense:
                continue

            output = self.__parseSense(sense)
            senseObjects.append(output)

        return senseObjects
