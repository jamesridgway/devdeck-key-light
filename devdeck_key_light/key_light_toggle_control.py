import logging
import os
import requests

from devdeck_core.controls.deck_control import DeckControl


class KeyLightToggleControl(DeckControl):
    def __init__(self, key_no, **kwargs):
        self.elgato = None
        self.__logger = logging.getLogger('devdeck')
        super().__init__(key_no, **kwargs)

    def initialize(self):
        self.__render_icon()

    def pressed(self):
        try:
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
        except requests.exceptions.ConnectionError as ex:
            self.__logger.warning("Error communicating with Elgato Key Light: %s", str(ex))
        self.__render_icon()


    def __render_icon(self):
        try:
            r = requests.get('http://{}:9123/elgato/lights'.format(self.settings['host']))
            data = r.json()
            with self.deck_context() as context:
                if data['lights'][0]['on'] == 1:
                    with context.renderer() as r:
                        r.image(os.path.join(os.path.dirname(__file__), "assets", 'key-light-on.png')).end()
                else:
                    with context.renderer() as r:
                        r.image(os.path.join(os.path.dirname(__file__), "assets", 'key-light-off.png')).end()
        except requests.exceptions.ConnectionError as ex:
            self.__logger.warning("Error communicating with Elgato Key Light: %s", str(ex))
            with self.deck_context() as context:
                with context.renderer() as r:
                    r \
                        .text('KEY LIGHT \nNOT FOUND') \
                        .color('red') \
                        .center_vertically() \
                        .center_horizontally() \
                        .font_size(85) \
                        .text_align('center') \
                        .end()

