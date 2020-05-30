import os
import re

import requests
from bs4 import BeautifulSoup


class Audio:
    BASE_URL = ''

    def __init__(self, lang, path):
        self.BASE_URL = f'https://{lang}.wiktionary.org/wiki/'
        self.path = '/home/tolga/.local/share/Anki2/User 1/collection.media'

    def get_audio(self, word: str) -> str:
        """
        Downloads the audio to the path and returns the anki formatted audio name
        if the download was succesful
        :return: The anki formatted audio string eg. [sound:word.ogg]
        or empty string if the audio failed
        :param word: The word for which the audio will be fetched
        """
        link = self.__get_audio_link(word)
        r = requests.get(link)

        if not r.ok:
            return ''

        with open(os.path.join(self.path, f'{word}.ogg'), 'wb') as f:
            f.write(r.content)
        return f'[sound:{word}.ogg]'

    def __get_audio_link(self, word: str) -> str:
        """ Gets the first .ogg link in the page
        :param word: The word for which the audio will be fetched
        :return: The URL of the correct .ogg link in the page
        """
        url = self.BASE_URL + word
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        return 'http:' + soup.find('a', href=re.compile(r'.*.ogg$'))['href']
