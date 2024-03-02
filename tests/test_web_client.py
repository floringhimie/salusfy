import pytest

from homeassistant.components.climate.const import (
    HVACMode,
    HVACAction
)

from salusfy import WebClient

# pylint: disable=missing-function-docstring


@pytest.fixture(name="payload")
def payload_fixture() -> dict:
    """Returns the default data for the tests"""
    return {
        'CH1currentSetPoint': 20.1,
        'CH1currentRoomTemp': 15.2,
        'frost': 8.5,
        'CH1heatOnOffStatus': "1",
        'CH1heatOnOff': "1",
        'CH1autoMode': "1"
    }


def test_extract_target_temperature(payload):
    actual = WebClient.convert_to_state(payload)

    assert actual.target_temperature == 20.1


def test_extract_current_temperature(payload):
    actual = WebClient.convert_to_state(payload)

    assert actual.current_temperature == 15.2


def test_extract_frost(payload):
    actual = WebClient.convert_to_state(payload)

    assert actual.frost == 8.5


def test_hvac_action_is_heating(payload):
    payload['CH1heatOnOffStatus'] = "1"
    payload['CH1heatOnOff'] = "1"
    payload['CH1autoMode'] = "1"
    actual = WebClient.convert_to_state(payload)

    assert actual.action == HVACAction.HEATING


def test_hvac_action_is_off(payload):
    payload['CH1heatOnOffStatus'] = "0"
    payload['CH1heatOnOff'] = "1"
    payload['CH1autoMode'] = "1"
    actual = WebClient.convert_to_state(payload)

    assert actual.action == HVACAction.IDLE


def test_hvac_mode_is_off(payload):
    payload['CH1heatOnOffStatus'] = "1"
    payload['CH1heatOnOff'] = "1"
    payload['CH1autoMode'] = "1"
    actual = WebClient.convert_to_state(payload)

    assert actual.mode == HVACMode.OFF


def test_hvac_mode_is_heat(payload):
    payload['CH1heatOnOffStatus'] = "1"
    payload['CH1heatOnOff'] = "0"
    payload['CH1autoMode'] = "1"
    actual = WebClient.convert_to_state(payload)

    assert actual.mode == HVACMode.HEAT
