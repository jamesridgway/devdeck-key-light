# DevDeck - Key Light
![CI](https://github.com/jamesridgway/devdeck-key-light/workflows/CI/badge.svg?branch=main)

Elgaato Key Light controls for [DevDeck](https://github.com/jamesridgway/devdeck).

## Installing
Simplify install *DevDeck - Key Light* into the same python environment that you have installed DevDeck.

    pip install devdeck-key-light

You can then update your DevDeck configuration to use decks and controls from this package.

## Controls

* `KeylightToggleControl`

   Can be used to toggle the state of an Elgato Key Light

## Configuration

Example configuration:

    decks:
      - serial_number: "ABC123"
        name: 'devdeck.decks.single_page_deck_controller.SinglePageDeckController'
        settings:
          controls:
            - name: 'devdeck_key_light.key_light_toggle_control.KeyLightToggleControl'
              key: 0
              settings:
                host: '192.168.1.23'
