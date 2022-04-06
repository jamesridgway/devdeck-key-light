import logging
import os
import requests

from xdg.BaseDirectory import *

from devdeck_core.controls.deck_control import DeckControl

defaultIconPath = os.path.join(xdg_config_dirs[0], 'devdeck/assets')

class KeyLightToggleControl(DeckControl):
    def __init__(self, key_no, **kwargs):
        self.elgato = None
        self.__logger = logging.getLogger('devdeck')
        super().__init__(key_no, **kwargs)
    
        self.iconPath = self.settings['iconPath'] or defaultIconPath

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
                        r.image(os.path.join(self.iconPath, self.settings['lightOnIcon'])).end()
                else:
                    with context.renderer() as r:
                        r.image(os.path.join(self.iconPath, self.settings['lightOffIcon'])).end()
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

    def settings_schema(self):
        return {
            'host': {
                'type': 'string',
                'required': True
            }
            'lightOnIcon': {
                'type': 'string',
                'required': True 
            }
            'ligtOffIcon': {
                'type': 'string',
                'required': True
            }
            'iconPath': {
                'type': 'string',
                'required': False
            }
        }
