import pytest
from unittest.mock import Mock

from salusfy import ( ThermostatEntity, State, WebClient )
from homeassistant.components.climate.const import (
    HVACMode
)

@pytest.fixture
def mock_client():
    state = State()
    state.current_temperature = 15.3
    state.target_temperature = 33.3
    
    mock = Mock(WebClient)
    mock.get_state.return_value = state

    return mock


@pytest.mark.asyncio
async def test_entity_returns_target_temp_from_web_client(mock_client):
    target = ThermostatEntity('mock', mock_client)

    await target.async_update()

    assert target.target_temperature == 33.3


@pytest.mark.asyncio
async def test_entity_delegates_set_temperature_web_client(mock_client):
    target = ThermostatEntity('mock', mock_client)

    await target.async_update()

    await target.async_set_temperature(temperature=29.9)

    mock_client.set_temperature.assert_called_once_with(29.9)
    assert target.target_temperature == 29.9


@pytest.mark.asyncio
async def test_entity_delegates_set_hvac_mode_to_web_client(mock_client):
    target = ThermostatEntity('mock', mock_client)

    await target.async_update()

    await target.async_set_hvac_mode(hvac_mode=HVACMode.HEAT)

    mock_client.set_hvac_mode.assert_called_once_with(HVACMode.HEAT)
    assert target.hvac_mode == HVACMode.HEAT