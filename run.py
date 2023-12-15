# To run this script to test the component:
# 1 Copy config.sample.py to config.py
# 2 Replace the username/password/deviceid (don't worry, this file will be ignored by git)
# 3 Run with `python run.py`

from custom_components.salusfy import climate

import config

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

print("Current: " + str(thermostat.current_temperature))
print("Target: " + str(thermostat.target_temperature))
print("HVAC Action: " + thermostat.hvac_action)
print("HVAC Mode: " + thermostat.hvac_mode)