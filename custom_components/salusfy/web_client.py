"""
Adds support for the Salus Thermostat units.
"""
import time
import logging
import re
import requests
import json 

from custom_components.salusfy.state import State

HVAC_MODE_HEAT = "heat"
HVAC_MODE_OFF = "off"

STATE_ON = "ON"
STATE_OFF = "OFF"

_LOGGER = logging.getLogger(__name__)

URL_LOGIN = "https://salus-it500.com/public/login.php"
URL_GET_TOKEN = "https://salus-it500.com/public/control.php"
URL_GET_DATA = "https://salus-it500.com/public/ajax_device_values.php"
URL_SET_DATA = "https://salus-it500.com/includes/set.php"

# Values from web interface
MIN_TEMP = 5
MAX_TEMP = 34.5

class WebClient:
    """Adapter around Salus IT500 web application."""

    def __init__(self, username, password, id):
        """Initialize the client."""
        self._username = username
        self._password = password
        self._id = id
        self._token = None
        
        self._session = requests.Session()


    def set_temperature(self, temperature):
        """Set new target temperature, via URL commands."""
        payload = {"token": self._token, "devId": self._id, "tempUnit": "0", "current_tempZ1_set": "1", "current_tempZ1": temperature}
        headers = {"content-type": "application/x-www-form-urlencoded"}
        try:
            self._session.post(URL_SET_DATA, data=payload, headers=headers)
            _LOGGER.info("Salusfy set_temperature OK")
        except:
            _LOGGER.error("Error Setting the temperature.")


    def set_hvac_mode(self, hvac_mode):
        """Set HVAC mode, via URL commands."""
        
        headers = {"content-type": "application/x-www-form-urlencoded"}
        if hvac_mode == HVAC_MODE_OFF:
            payload = {"token": self._token, "devId": self._id, "auto": "1", "auto_setZ1": "1"}
            try:
                self._session.post(URL_SET_DATA, data=payload, headers=headers)
            except:
                _LOGGER.error("Error Setting HVAC mode OFF.")
        elif hvac_mode == HVAC_MODE_HEAT:
            payload = {"token": self._token, "devId": self._id, "auto": "0", "auto_setZ1": "1"}
            try:
                self._session.post(URL_SET_DATA, data=payload, headers=headers)
            except:
                _LOGGER.error("Error Setting HVAC mode.")

        _LOGGER.info("Setting the HVAC mode.")


    def get_token(self):
        """Get the Session Token of the Thermostat."""
        payload = {"IDemail": self._username, "password": self._password, "login": "Login", "keep_logged_in": "1"}
        headers = {"content-type": "application/x-www-form-urlencoded"}
        
        try:
            self._session.post(URL_LOGIN, data=payload, headers=headers)
            params = {"devId": self._id}
            getTkoken = self._session.get(URL_GET_TOKEN,params=params)
            result = re.search('<input id="token" type="hidden" value="(.*)" />', getTkoken.text)
            _LOGGER.info("Salusfy get_token OK")
            self._token = result.group(1)
        except:
            _LOGGER.error("Error getting the session token.")


    def get_state(self):
        if self._token is None:
            self.get_token()
        
        params = {"devId": self._id, "token": self._token, "&_": str(int(round(time.time() * 1000)))}
        try:
            r = self._session.get(url = URL_GET_DATA, params = params)
            if not r:
                _LOGGER.error("Could not get data from Salus.")
                return None
        except:
            _LOGGER.error("Error Getting the data from Web. Please check the connection to salus-it500.com manually.")
            return None
            
        try:
            data = json.loads(r.text)
            _LOGGER.info("Salusfy get_data output " + r.text)

            state = State()
            state.target_temperature = float(data["CH1currentSetPoint"])
            state.current_temperature = float(data["CH1currentRoomTemp"])
            state.frost = float(data["frost"])
            
            status = data['CH1heatOnOffStatus']
            if status == "1":
                state.status = STATE_ON
            else:
                state.status = STATE_OFF
            
            mode = data['CH1heatOnOff']
            if mode == "1":
                state.current_operation_mode = STATE_OFF
            else:
                state.current_operation_mode = STATE_ON
            
            return state
        except:
            self.get_token()
            return self.get_state()

