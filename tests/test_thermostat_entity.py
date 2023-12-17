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

@pytest.fixture
def mock_ha_client():
    mock = MagicMock()

    mock.configure_mock(
        **{
            "current_temperature.return_value": 21.1
        }
    )
    
    return mock

def test_entity_returns_target_temp_from_web_client(mock_client, mock_ha_client):
    target = ThermostatEntity('mock', mock_client, mock_ha_client)

    assert target.target_temperature == 33.3


def test_entity_returns_target_temp_from_home_assistant_client(mock_client, mock_ha_client):
    target = ThermostatEntity('mock', mock_client, mock_ha_client)

    assert target.current_temperature == 21.1


def test_entity_call_salus_client_only_once(mock_client, mock_ha_client):
    target = ThermostatEntity('mock', mock_client, mock_ha_client)

    target.update()
    target.update()

    mock_client.get_state.assert_called_once()
    assert target.target_temperature == 33.3


def test_entity_delegates_set_temperature_salus_client(mock_client, mock_ha_client):
    target = ThermostatEntity('mock', mock_client, mock_ha_client)

    target.set_temperature(temperature=29.9)

    mock_client.set_temperature.assert_called_once_with(29.9)
    assert target.target_temperature == 29.9


def test_entity_delegates_set_hvac_mode_to_salus_client(mock_client, mock_ha_client):
    target = ThermostatEntity('mock', mock_client, mock_ha_client)

    target.set_hvac_mode(hvac_mode=HVAC_MODE_HEAT)

    mock_client.set_hvac_mode.assert_called_once_with(HVAC_MODE_HEAT)
    assert target.hvac_mode == HVAC_MODE_HEAT