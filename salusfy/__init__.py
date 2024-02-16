"""The Salus component."""

from .state import State
from .web_client import (
    WebClient,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    STATE_ON,
    STATE_OFF
)
from .mock_web_client import MockWebClient
from .thermostat_entity import ThermostatEntity
from .client import Client
from .ha_temperature_client import HaTemperatureClient
from .mock_ha_temperature_client import MockHaTemperatureClient