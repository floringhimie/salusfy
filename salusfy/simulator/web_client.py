"""
Adds support for simulating the Salus Thermostats.
"""
import logging

from homeassistant.components.climate.const import (
    HVACMode,
)

from .. import (
    State,
    STATE_ON,
    STATE_OFF
)


_LOGGER = logging.getLogger(__name__)


class WebClient:
    """Mocks requests to Salus web application"""

    def __init__(self):
        """Initialize the client."""
        self._state = State()
        self._state.target_temperature = 20.1
        self._state.current_temperature = 15.1
        self._state.frost = 10.1


    def set_temperature(self, temperature):
        """Set new target temperature."""
        
        _LOGGER.info("Setting temperature to %.1f...", temperature)
        
        self._state.target_temperature = temperature


    def set_hvac_mode(self, hvac_mode):
        """Set HVAC mode, via URL commands."""
        
        _LOGGER.info("Setting the HVAC mode to %s...", hvac_mode)

        if hvac_mode == HVACMode.OFF:
            self._state.current_operation_mode = STATE_OFF
        elif hvac_mode == HVACMode.HEAT:
            self._state.current_operation_mode = STATE_ON


    def get_state(self):
        """Retrieves the mock status"""
        return self._state
