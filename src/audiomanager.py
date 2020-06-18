import os
import re
from pydub import AudioSegment
from pydub import effects

import requests
from bs4 import BeautifulSoup


class AudioManager:
    def __init__(self, lang: str, path: str, normalize: bool):
        self.BASE_URL = f'https://{lang}.wiktionary.org/wiki/'
        self.path = path
        self.normalize = normalize

    def get_audio(self, word: str) -> str:
        """
        Downloads the audio to the path and returns the anki formatted audio name
        if the download was succesful
        :return: The anki formatted audio string eg. [sound:word.ogg]
        or empty string if the audio failed
        :param word: The word for which the audio will be fetched
        """
        try:
            link = self.__get_audio_link(word)

            r = requests.get(link)

            if not r.ok:
                return ''
        except Exception:
            return ''

        file_path = os.path.join(self.path, f'{word}.ogg')
        with open(file_path, 'wb') as f:
            f.write(r.content)

        if self.normalize:
            effects.normalize(AudioSegment.from_ogg(file_path)).export(file_path)

        return f'[sound:{word}.ogg]'

    def __get_audio_link(self, word: str) -> str:
        """ Gets the first .ogg link in the page
        :param word: The word for which the audio will be fetched
        :return: The URL of the correct .ogg link in the page
        """
        url = self.BASE_URL + word
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        return 'http:' + soup.find('a', href=re.compile(r'.*.ogg$'))['href']
