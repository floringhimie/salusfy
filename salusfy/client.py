"""
Client which wraps the web client but handles
the retrieval of current temperature by calling
a specialized client.
"""
import logging

from homeassistant.components.climate.const import (
    HVACMode,
    HVACAction,
)

from . import (
    WebClient,
    HaTemperatureClient,
    State,
)

_LOGGER = logging.getLogger(__name__)


class Client:
    """Mocks requests to Salus web application"""

    def __init__(
            self,
            web_client: WebClient,
            temperature_client: HaTemperatureClient):
        """Initialize the client."""
        self._state = None
        self._web_client = web_client
        self._temperature_client = temperature_client

    async def set_temperature(self, temperature: float) -> None:
        """Set new target temperature."""

        _LOGGER.info("Delegating set_temperature to web client...")

        await self._web_client.set_temperature(temperature)

        self._state.target_temperature = temperature

        self.assume_hvac_action()

    async def set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set HVAC mode, via URL commands."""

        _LOGGER.info("Delegating set_hvac_mode to web client...")

        await self._web_client.set_hvac_mode(hvac_mode)

        self._state.mode = hvac_mode

        self.assume_hvac_action()

    def assume_hvac_action(self) -> None:
        """Assumes what the hvac action is based on
        the mode and current/target temperatures"""
        if self._state.mode == HVACMode.OFF:
            _LOGGER.info("Assuming action is IDLE...")
            self._state.action = HVACAction.IDLE
            return

        if self._state.target_temperature > self._state.current_temperature:
            _LOGGER.info(
                "Assuming action is HEATING based on target temperature...")
            self._state.action = HVACAction.HEATING
            return

        _LOGGER.info("Assuming action is IDLE based on target temperature...")
        self._state.action = HVACAction.IDLE

    async def get_state(self) -> State:
        """Retrieves the status"""

        if self._state is None:
            _LOGGER.info("Delegating get_state to web client...")
            self._state = await self._web_client.get_state()

        _LOGGER.info("Updating current temperature from temperature client...")
        self._state.current_temperature = await self._temperature_client.current_temperature()

        return self._state
