# pylint: disable=too-few-public-methods
# pylint: disable=too-many-return-statements

class ConfigAdapter:
    """Simulates how Home Assistant loads configuration"""

    def __init__(self, config):
        self._config = config

    def get(self, key: str) -> any:
        """Returns the config value based on the Home Assistant key"""

        if key == 'name':
            return 'Simulator'

        if key == 'id':
            return self._config.DEVICE_ID

        if key == 'username':
            return self._config.USERNAME

        if key == 'password':
            return self._config.PASSWORD

        if key == 'simulator':
            if hasattr(self._config, 'SIMULATOR'):
                return self._config.SIMULATOR
            return False

        if key == 'enable_temperature_client':
            if hasattr(self._config, 'ENABLE_TEMPERATURE_CLIENT'):
                return self._config.ENABLE_TEMPERATURE_CLIENT
            return False

        if key == 'host':
            return self._config.HOST

        if key == 'entity_id':
            return self._config.ENTITY_ID

        if key == 'access_token':
            return self._config.ACCESS_TOKEN

        return 'Unknown'
