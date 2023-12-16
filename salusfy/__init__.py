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
from .ha_web_client import HaWebClient
from .mock_ha_web_client import MockHaWebClient