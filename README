# Anki Language Card Generator
Generates anki cards semi-automatically using the [lexicala api](https://api.lexicala.com/).

Still under construction. Not really tested for any language combination other than Dutch to English.

## Functionality Overview
Given a txt file with an L2 (the language you are learning) word at each line:

* Grabs every listed L1 (your own language) meaning, native definitions and example sentences from the Lexicala API
* Downloads audio from wiktionary, normalizes the volume of the audio.
* Attempts to make a cloze deletion in the example sentence.
* Produces a csv file that can be imported to Anki or automatically adds the cards to your deck through [AnkiConnect](https://ankiweb.net/shared/info/2055492159).

## Installation
TODO

## Getting Started
TODO

## Configuration
All configuration is done via the `config.ini` file.
If you want to provide your own file, run the program as
`ankigen.py -c '/path/to/file'`. This file should be
configured before a run. Refer to the example config file.

## Future Development Plans
This is what I am planning to add to this app in the future for my own use. If you have a cool idea to expand the program, please make an issue or a Pull Request. The same goes if you find any bugs in the program as well.
* Devise a system to personalize the card fields
* Create a GUI
* Transform this into an actual Anki Add-on
* Make a proper logging system

### Dependencies
Can be installed via `pip install -r requirements.txt`

* python == 3.8
* beautifulsoup4 == 4.6.0
* pydub == 0.24.0
* requests == 2.20.0


