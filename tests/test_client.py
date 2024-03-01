from unittest.mock import Mock
import pytest

from homeassistant.components.climate.const import (
    HVACMode,
    HVACAction
)

from salusfy import (Client, State, WebClient, HaTemperatureClient)


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
async def test_client_returns_target_temp_from_web_client(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    actual = await target.get_state()

    assert actual.target_temperature == 33.3


@pytest.mark.asyncio
async def test_client_returns_target_temp_from_home_assistant_client(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    actual = await target.get_state()

    assert actual.current_temperature == 21.1


@pytest.mark.asyncio
async def test_client_call_salus_client_only_once(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.get_state()
    await target.get_state()

    mock_client.get_state.assert_called_once()

    actual = await target.get_state()
    assert actual.target_temperature == 33.3


@pytest.mark.asyncio
async def test_client_delegates_set_temperature_salus_client(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.get_state()

    await target.set_temperature(temperature=29.9)

    mock_client.set_temperature.assert_called_once_with(29.9)


@pytest.mark.asyncio
async def test_client_delegates_set_hvac_mode_to_salus_client(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.get_state()

    await target.set_hvac_mode(hvac_mode=HVACMode.HEAT)

    mock_client.set_hvac_mode.assert_called_once_with(HVACMode.HEAT)


@pytest.mark.asyncio
async def test_client_assumes_hvac_action_as_idle_when_mode_is_off(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.get_state()

    await target.set_hvac_mode(hvac_mode=HVACMode.OFF)

    actual = await target.get_state()

    assert actual.action == HVACAction.IDLE


@pytest.mark.asyncio
async def test_client_sets_hvac_mode(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.get_state()

    await target.set_hvac_mode(hvac_mode=HVACMode.OFF)

    actual = await target.get_state()

    assert actual.mode == HVACMode.OFF


@pytest.mark.asyncio
async def test_client_assumes_hvac_action_as_heat_when_mode_is_heat_and_target_temp_is_high(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.get_state()

    await target.set_temperature(temperature=30)
    await target.set_hvac_mode(hvac_mode=HVACMode.HEAT)

    actual = await target.get_state()

    assert actual.action == HVACAction.HEATING


@pytest.mark.asyncio
async def test_client_assumes_hvac_action_as_idle_when_mode_is_heat_and_target_temp_is_low(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.get_state()

    await target.set_temperature(temperature=4)
    await target.set_hvac_mode(hvac_mode=HVACMode.HEAT)

    actual = await target.get_state()

    assert actual.action == HVACAction.IDLE


@pytest.mark.asyncio
async def test_client_assumes_hvac_action_as_heat_when_mode_is_heat_and_target_temp_is_set_high(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.get_state()

    await target.set_hvac_mode(hvac_mode=HVACMode.HEAT)
    await target.set_temperature(temperature=33)

    actual = await target.get_state()

    assert actual.action == HVACAction.HEATING


@pytest.mark.asyncio
async def test_client_assumes_hvac_action_as_idle_when_mode_is_heat_and_target_temp_is_set_low(mock_client, mock_ha_client):
    target = Client(mock_client, mock_ha_client)

    await target.get_state()

    await target.set_hvac_mode(hvac_mode=HVACMode.HEAT)
    await target.set_temperature(temperature=4)

    actual = await target.get_state()

    assert actual.action == HVACAction.IDLE
