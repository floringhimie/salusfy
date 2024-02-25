"""
Client which wraps the web client but handles
the retrieval of current temperature by calling
a specialized client.
"""
import logging
from .web_client import WebClient
from .ha_temperature_client import HaTemperatureClient

_LOGGER = logging.getLogger(__name__)

class Client:
    """Mocks requests to Salus web application"""

    def __init__(self, web_client : WebClient, temperature_client : HaTemperatureClient):
        """Initialize the client."""
        self._state = None
        self._web_client = web_client
        self._temperature_client = temperature_client


    async def set_temperature(self, temperature):
        """Set new target temperature."""
        
        _LOGGER.info("Delegating set_temperature to web client...")

        await self._web_client.set_temperature(temperature)


    async def set_hvac_mode(self, hvac_mode):
        """Set HVAC mode, via URL commands."""
        
        _LOGGER.info("Delegating set_hvac_mode to web client...")

        await self._web_client.set_hvac_mode(hvac_mode)


    async def get_state(self):
        """Retrieves the status"""
        
        if self._state is None:
            _LOGGER.info("Delegating get_state to web client...")
            self._state = await self._web_client.get_state()
        
        _LOGGER.info("Updating current temperature from temperature client...")
        self._state.current_temperature = await self._temperature_client.current_temperature()

        return self._state

    
    async def close(self):
        """Closes the client session"""
        await self._web_client.close()