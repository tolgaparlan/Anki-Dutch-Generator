import requests
import re
import os
from bs4 import BeautifulSoup


class Audio():
    BASE_URL = ''

    def __init__(self, lang, path):
        self.BASE_URL = f'https://{lang}.wiktionary.org/wiki/'
        self.path = '/home/tolga/.local/share/Anki2/User 1/collection.media'

    # Downloads the audio to the path and returns the anki formatted
    # audio name if the download was succesful
    def getAudio(self, word):
        link = self.__getAudioLink(word)
        r = requests.get(link)

        if not r.ok:
            return ''

        with open(os.path.join(self.path, f'{word}.ogg'), 'wb') as f:
            f.write(r.content)
        return f'[sound:{word}.ogg]'

    def __getAudioLink(self, word):
        ''' Gets the first .ogg link in the page '''
        url = self.BASE_URL + word
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        return 'http:' + soup.find('a', href=re.compile(r'.*.ogg$'))['href']
