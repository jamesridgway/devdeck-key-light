
import os
import requests

from devdeck_core.controls.deck_control import DeckControl


class KeyLightToggleControl(DeckControl):
    def __init__(self, key_no, **kwargs):
        self.elgato = None
        super().__init__(key_no, **kwargs)

    def initialize(self):
        self.__render_icon()

    def pressed(self):
        r = requests.get('http://{}:9123/elgato/lights'.format(self.settings['host']))
        current_state = r.json()

        data = {
            'lights': [
                {
                    'on': 0 if current_state['lights'][0]['on'] == 1 else 1
                }
            ],
            'numberOfLights': 1
        }
        requests.put(
            'http://{}:9123/elgato/lights'.format(self.settings['host']),
            json=data)
        self.__render_icon()

    def __render_icon(self):
        r = requests.get('http://{}:9123/elgato/lights'.format(self.settings['host']))
        data = r.json()
        with self.deck_context() as context:
            if data['lights'][0]['on'] == 1:
                with context.renderer() as r:
                    r.image(os.path.join(os.path.dirname(__file__), "assets", 'key-light-on.png')).end()
            else:
                with context.renderer() as r:
                    r.image(os.path.join(os.path.dirname(__file__), "assets", 'key-light-off.png')).end()

