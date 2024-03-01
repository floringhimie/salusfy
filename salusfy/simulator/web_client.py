"""
Adds support for simulating the Salus Thermostats.
"""
import logging

from homeassistant.components.climate.const import HVACMode

from ..state import State


_LOGGER = logging.getLogger(__name__)


class WebClient:
    """Mocks requests to Salus web application"""

    def __init__(self):
        """Initialize the client."""
        self._state = State()
        self._state.target_temperature = 20.1
        self._state.current_temperature = 15.1
        self._state.frost = 10.1


    async def set_temperature(self, temperature: float) -> None:
        """Set new target temperature."""
        
        _LOGGER.info("Setting temperature to %.1f...", temperature)
        
        self._state.target_temperature = temperature


    async def set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set HVAC mode, via URL commands."""
        
        _LOGGER.info("Setting the HVAC mode to %s...", hvac_mode)

        self._state.mode = hvac_mode


    async def get_state(self) -> State:
        """Retrieves the mock status"""
        return self._state
