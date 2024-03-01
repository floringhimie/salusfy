"""
Adds support for the Salus Thermostat units.
"""
import time
import logging
import re
import aiohttp
import json

from .state import State

from homeassistant.components.climate.const import (
    HVACMode,
    HVACAction,
)


_LOGGER = logging.getLogger(__name__)

URL_LOGIN = "https://salus-it500.com/public/login.php"
URL_GET_TOKEN = "https://salus-it500.com/public/control.php"
URL_GET_DATA = "https://salus-it500.com/public/ajax_device_values.php"
URL_SET_DATA = "https://salus-it500.com/includes/set.php"

# Values from web interface
MIN_TEMP = 5
MAX_TEMP = 34.5
MAX_TOKEN_AGE_SECONDS = 60 * 10


class WebClient:
    """Adapter around Salus IT500 web application."""

    def __init__(self, username, password, id):
        """Initialize the client."""
        self._username = username
        self._password = password
        self._id = id
        self._token = None
        self._tokenRetrievedAt = None

    async def set_temperature(self, temperature: float) -> None:
        """Set new target temperature, via URL commands."""

        _LOGGER.info("Setting the temperature to %.1f...", temperature)

        async with aiohttp.ClientSession() as session:
            token = await self.obtain_token(session)

            payload = {
                "token": token,
                "devId": self._id,
                "tempUnit": "0",
                "current_tempZ1_set": "1",
                "current_tempZ1": temperature}
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            try:
                await session.post(URL_SET_DATA, data=payload, headers=headers)
                _LOGGER.info("Salusfy set_temperature: OK")
            except BaseException:
                _LOGGER.error("Error Setting the temperature.")

    async def set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set HVAC mode, via URL commands."""

        _LOGGER.info("Setting the HVAC mode to %s...", hvac_mode)

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        auto = "1"
        if hvac_mode == HVACMode.OFF:
            auto = "1"
        elif hvac_mode == HVACMode.HEAT:
            auto = "0"

        async with aiohttp.ClientSession() as session:
            token = await self.obtain_token(session)

            payload = {
                "token": token,
                "devId": self._id,
                "auto": auto,
                "auto_setZ1": "1"}
            try:
                await session.post(URL_SET_DATA, data=payload, headers=headers)
            except BaseException:
                _LOGGER.error("Error Setting HVAC mode to %s", hvac_mode)

    async def obtain_token(self, session: str) -> str:
        """Gets the existing session token of the thermostat or retrieves a new one if expired."""

        if self._token is None:
            _LOGGER.info("Retrieving token for the first time this session...")
            await self.get_token(session)
            return self._token

        if self._tokenRetrievedAt > time.time() - MAX_TOKEN_AGE_SECONDS:
            _LOGGER.info("Using cached token...")
            return self._token

        _LOGGER.info("Token has expired, getting new one...")
        await self.get_token(session)
        return self._token

    async def get_token(self, session: str) -> None:
        """Get the Session Token of the Thermostat."""

        _LOGGER.info("Getting token from Salus...")

        payload = {
            "IDemail": self._username,
            "password": self._password,
            "login": "Login",
            "keep_logged_in": "1"}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            await session.post(URL_LOGIN, data=payload, headers=headers)
            params = {"devId": self._id}
            getTkoken = await session.get(URL_GET_TOKEN, params=params)
            body = await getTkoken.text()
            result = re.search(
                '<input id="token" type="hidden" value="(.*)" />', body)
            _LOGGER.info("Salusfy get_token OK")
            self._token = result.group(1)
            self._tokenRetrievedAt = time.time()
        except Exception as e:
            self._token = None
            self._tokenRetrievedAt = None
            _LOGGER.error("Error getting the session token.")
            _LOGGER.error(e)

    async def get_state(self) -> State:
        """Retrieve the current state from the Salus gateway"""

        _LOGGER.info("Retrieving current state from Salus Gateway...")

        data = await self.get_state_data()

        state = State()
        state.target_temperature = float(data["CH1currentSetPoint"])
        state.current_temperature = float(data["CH1currentRoomTemp"])
        state.frost = float(data["frost"])

        status = data['CH1heatOnOffStatus']
        if status == "1":
            state.action = HVACAction.HEATING
        else:
            state.action = HVACAction.IDLE

        mode = data['CH1heatOnOff']
        if mode == "1":
            state.mode = HVACMode.OFF
        else:
            state.mode = HVACMode.HEAT

        return state

    async def get_state_data(self) -> dict:
        """Retrieves the raw state from the Salus gateway"""

        _LOGGER.info("Retrieving raw state from Salus Gateway...")

        async with aiohttp.ClientSession() as session:
            token = await self.obtain_token(session)

            params = {"devId": self._id, "token": token,
                      "&_": str(int(round(time.time() * 1000)))}
            try:
                r = await session.get(url=URL_GET_DATA, params=params)
                if not r:
                    _LOGGER.error("Could not get data from Salus.")
                    return None
            except BaseException:
                _LOGGER.error(
                    "Error Getting the data from Web. Please check the connection to salus-it500.com manually.")
                return None

            body = await r.text()
            _LOGGER.info("Salusfy get_data output %s", body)
            data = json.loads(body)

            return data
