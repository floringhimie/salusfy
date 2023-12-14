# To run this script to test the component:
# 1 Copy config.sample.py to config.py
# 2 Replace the username/password/deviceid (don't worry, this file will be ignored by git)
# 3 Run with `python run.py`

from custom_components.salusfy.thermostat_entity import ThermostatEntity
from custom_components.salusfy.web_client import WebClient

import config

client = WebClient(config.USERNAME, config.PASSWORD, config.DEVICE_ID)
thermostat = ThermostatEntity("thermostat", client)

print("Current: " + str(thermostat.current_temperature))
print("Target: " + str(thermostat.target_temperature))
print("HVAC Action: " + thermostat.hvac_action)
print("HVAC Mode: " + thermostat.hvac_mode)