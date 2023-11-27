import abc
import logging
import os
import requests

from devdeck_core.controls.deck_control import DeckControl


class _BrightnessBase(abc.ABC, DeckControl):
    def __init__(self, key_no, **kwargs):
        self.elgato = None
        self.__logger = logging.getLogger('devdeck')
        super().__init__(key_no, **kwargs)

    @property
    @abc.abstractmethod
    def image_file(self):
        'Image file to render. Relative path to assets directory.'
        ...

    @property
    def endpoint(self):
        return 'http://{}:9123/elgato/lights'.format(self.settings['host'])

    def initialize(self):
        with self.deck_context() as context:
            with context.renderer() as r:
                r.image(os.path.join(os.path.dirname(__file__), 'assets', self.image_file)).end()

    @property
    def brightness(self):
        try:
            r = requests.get(self.endpoint)
        except requests.exceptions.ConnectionError as ex:
            self.__logger.warning("Error communicating with Elgato Key Light: %s", str(ex))
            return 0
        return r.json()['lights'][0]['brightness']

    @brightness.setter
    def brightness(self, value):
        if not 0 <= value <= 100:
            raise ValueError('Valid brightness values are between 0 and 100 inclusive.')
        data = {
            'lights': [
                {
                    'brightness': int(value),
                }
            ],
            'numberOfLights': 1
        }
        try:
            requests.put(self.endpoint, json=data)
        except requests.exceptions.ConnectionError as ex:
            self.__logger.warning("Error communicating with Elgato Key Light: %s", str(ex))


class Increase(_BrightnessBase):
    @property
    def image_file(self):
        return 'brightness-high.png'

    def pressed(self):
        self.brightness = min(100, self.brightness + self.settings['step'])


class Decrease(_BrightnessBase):
    @property
    def image_file(self):
        return 'brightness-low.png'

    def pressed(self):
        self.brightness = max(0, self.brightness - self.settings['step'])