import os

from anki.hooks import addHook
from aqt import mw
from aqt.utils import showInfo

from anki_generate.api import APIAccess
from anki_generate.audio import Audio
from anki_generate.output import OutputWriter

assets = os.path.join(os.path.dirname(__file__), "assets")

# Read the config file options
config = mw.addonManager.getConfig(__name__)

# Initialize the classes
api = APIAccess(config['language']['L2'], config['language']['L1'],
                config['credentials']['username'],
                config['credentials']['password'])

output_writer = OutputWriter()


def on_generate(editor):
    """
    Handler for the generate button.
    """
    showInfo("Pressed the button")

# Add the button and the shortcut
def add_generate_button(buttons, editor):
    editor._links['generate'] = on_generate
    return buttons + [editor._addButton(
        os.path.join(assets, 'icon.png'),
        "generate",  # link name
        "generate")]

addHook("setupEditorButtons", add_generate_button)
