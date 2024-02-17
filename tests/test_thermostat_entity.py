import pytest
from unittest.mock import MagicMock

from salusfy import ( ThermostatEntity, State )
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT
)

@pytest.fixture
def mock_client():
    mock = MagicMock()

    state = State()
    state.current_temperature = 15.3
    state.target_temperature = 33.3
    mock.configure_mock(
        **{
            "get_state.return_value": state
        }
    )

    return mock


def test_entity_returns_target_temp_from_web_client(mock_client):
    target = ThermostatEntity('mock', mock_client)

    assert target.target_temperature == 33.3


def test_entity_delegates_set_temperature_web_client(mock_client):
    target = ThermostatEntity('mock', mock_client)

    target.set_temperature(temperature=29.9)

    mock_client.set_temperature.assert_called_once_with(29.9)
    assert target.target_temperature == 29.9


def test_entity_delegates_set_hvac_mode_to_web_client(mock_client):
    target = ThermostatEntity('mock', mock_client)

    target.set_hvac_mode(hvac_mode=HVAC_MODE_HEAT)

    mock_client.set_hvac_mode.assert_called_once_with(HVAC_MODE_HEAT)
    assert target.hvac_mode == HVAC_MODE_HEAT