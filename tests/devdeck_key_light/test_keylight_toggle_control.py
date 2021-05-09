import vcr
from devdeck_core.mock_deck_context import mock_context, assert_rendered
from tests.testing_utils import TestingUtils

from devdeck_key_light.key_light_toggle_control import KeyLightToggleControl


class TestKeyLightToggleControl:
    @vcr.use_cassette('tests/fixtures/test_key_light_toggle/test_initialize_sets_icon.yaml')
    def test_initialize_sets_icon(self):
        settings = {
            'host': '192.168.2.25'
        }
        control = KeyLightToggleControl(0, **settings)
        with mock_context(control) as ctx:
            control.initialize()
            assert_rendered(ctx, TestingUtils.get_filename('../devdeck_key_light/assets/key-light-on.png'))

    @vcr.use_cassette('tests/fixtures/test_key_light_toggle/test_initialize_sets_icon_off.yaml')
    def test_initialize_sets_icon_off(self):
        settings = {
            'host': '192.168.2.25'
        }
        control = KeyLightToggleControl(0, **settings)
        with mock_context(control) as ctx:
            control.initialize()
            assert_rendered(ctx, TestingUtils.get_filename('../devdeck_key_light/assets/key-light-off.png'))
