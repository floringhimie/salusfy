import pytest
from unittest.mock import Mock

from salusfy import ( Client, State, WebClient, HaTemperatureClient )
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


@pytest.fixture
def mock_ha_client():
    mock = Mock(HaTemperatureClient)

    mock.current_temperature.return_value = 21.1
    
    return mock


@pytest.mark.asyncio
async def test_entity_returns_target_temp_from_web_client(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    actual = await target.get_state()

    assert actual.target_temperature == 33.3


@pytest.mark.asyncio
async def test_entity_returns_target_temp_from_home_assistant_client(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    actual = await target.get_state()
    
    assert actual.current_temperature == 21.1


@pytest.mark.asyncio
async def test_entity_call_salus_client_only_once(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.get_state()
    await target.get_state()

    mock_client.get_state.assert_called_once()

    actual = await target.get_state()
    assert actual.target_temperature == 33.3


@pytest.mark.asyncio
async def test_entity_delegates_set_temperature_salus_client(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.set_temperature(temperature=29.9)

    mock_client.set_temperature.assert_called_once_with(29.9)


@pytest.mark.asyncio
async def test_entity_delegates_set_hvac_mode_to_salus_client(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.set_hvac_mode(hvac_mode=HVACMode.HEAT)

    mock_client.set_hvac_mode.assert_called_once_with(HVACMode.HEAT)