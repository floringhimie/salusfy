# To run this script to test the component:
# 1 Copy config.sample.py to config.py
# 2 Replace the username/password/deviceid (don't worry, this file will be ignored by git)
# 3 Run with `python run.py`

from custom_components.salusfy import climate

from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
)

import config

import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class ConfigAdapter:
    def __init__(self, config):
        self._config = config

    
    def get(self, key):
        if (key == 'name'):
            return 'Simulator'
        
        if (key == 'id'):
            return self._config.DEVICE_ID
        
        if (key == 'username'):
            return self._config.USERNAME

        if (key == 'password'):
            return self._config.PASSWORD

        if (key == 'simulator'):
            return self._config.SIMULATOR
        
        if (key == 'host'):
            return self._config.HOST

        if (key == 'entity_id'):
            return self._config.ENTITY_ID

        if (key == 'access_token'):
            return self._config.ACCESS_TOKEN
        
        
class EntityRegistry:
    def __init__(self):
        self._entities = []
    
    def register(self, list):
        self._entities.extend(list)
    
    def first(self):
        return self._entities[0]


registry = EntityRegistry()
config_adapter = ConfigAdapter(config)

climate.setup_platform(None, config_adapter, add_entities=registry.register, discovery_info=None)

thermostat = registry.first()

thermostat.update()
thermostat.update()

thermostat.set_hvac_mode(HVAC_MODE_HEAT)
thermostat.set_temperature(temperature=9.8)

print("Current: " + str(thermostat.current_temperature))
print("Target: " + str(thermostat.target_temperature))
print("HVAC Action: " + thermostat.hvac_action)
print("HVAC Mode: " + thermostat.hvac_mode)