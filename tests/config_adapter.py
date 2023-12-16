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