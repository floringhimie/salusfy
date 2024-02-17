# To run this script to test the component:
# 1 Copy config.sample.py to config.py
# 2 Replace the username/password/deviceid (don't worry, this file will be ignored by git)
# 3 Run with `python run.py`

from salusfy import climate
from tests.config_adapter import ConfigAdapter
from tests.entity_registry import EntityRegistry

from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
)

import config

import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

registry = EntityRegistry()
config_adapter = ConfigAdapter(config)

climate.setup_platform(None, config_adapter, add_entities=registry.register, discovery_info=None)

thermostat = registry.first

thermostat.update()
thermostat.update()

thermostat.set_hvac_mode(HVAC_MODE_HEAT)
thermostat.set_temperature(temperature=9.8)

print("Current: " + str(thermostat.current_temperature))
print("Target: " + str(thermostat.target_temperature))
print("HVAC Action: " + thermostat.hvac_action)
print("HVAC Mode: " + thermostat.hvac_mode)