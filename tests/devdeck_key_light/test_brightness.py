import vcr
from devdeck_core.mock_deck_context import mock_context, assert_rendered
from tests.testing_utils import TestingUtils

from devdeck_key_light.brightness import Increase


class TestBrightness:
    def test_simple_increase(self):
        settings = {
            'host': '192.168.2.25',
            'step': 20,
        }
        control = Increase(0, **settings)
        with vcr.use_cassette('tests/fixtures/test_brightness/test_simple_increase.yaml',
                              match_on=['uri', 'method', 'body']) as cass:
            with mock_context(control) as ctx:
                control.initialize()
                assert_rendered(ctx, TestingUtils.get_filename(
                    '../devdeck_key_light/assets/brightness-high.png'))
                control.pressed()
            assert cass.all_played
