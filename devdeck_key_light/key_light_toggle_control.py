import logging
import os
import requests
import time
import threading

from devdeck_core.controls.deck_control import DeckControl


class KeyLightToggleControl(DeckControl):
    def __init__(self, key_no, **kwargs):
        self.elgato = None
        self.__logger = logging.getLogger('devdeck')
        super().__init__(key_no, **kwargs)

    def initialize(self):

        self.watcherThread = threading.Thread(target=self.watcher)
        self.watcherThread.start()
        
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
    
    def watcher(self):
        self.state = None

        while True:
            try:
                r = requests.get('http://{}:9123/elgato/lights'.format(self.settings['host']))
                data = r.json()

                with self.deck_context() as context:
                    if self.state != data['lights'][0]['on']:
                        self.state = data['lights'][0]['on']
            except requests.exceptions.ConnectionError as ex:
                self.__logger.warning("Error communicating with ELgato Key Light: %s", str(ex))
                self.state = 9
            
            self.render_icon(self.state)
            time.sleep(0.5)
        self.__logger.error("We should never exit the thread - oops!")
        exit(1)

    def render_icon(self, state):
        self.state = state

        with self.deck_context() as context:
            with context.renderer() as r:
                if self.state == 9:
                    r \
                        .text('KEY LIGHT \nNOT FOUND') \
                        .color('red') \
                        .center_vertically() \
                        .center_horizontally() \
                        .font_size(85) \
                        .text_align('center') \
                        .end()
                elif self.state == 1:
                    r.image(os.path.join(os.path.dirname(__file__), "assets", 'key-light-on.png')).end()
                else:
                    r.image(os.path.join(os.path.dirname(__file__), "assets", 'key-light-off.png')).end()


