import pytest
from unittest.mock import MagicMock

from salusfy import ( ThermostatEntity, State )


def test_entity_is_registered():
    mock_client = MagicMock()
    mock_ha_client = MagicMock()

    state = State()
    state.current_temperature = 15.3
    state.target_temperature = 33.3
    mock_client.configure_mock(
        **{
            "get_state.return_value": state
        }
    )

    mock_ha_client.configure_mock(
        **{
            "current_temperature.return_value": 21.1
        }
    )

    target = ThermostatEntity('mock', mock_client, mock_ha_client)
    
    assert target.current_temperature == 21.1
    assert target.target_temperature == 33.3
    # mock_table.insert.assert_called_once()