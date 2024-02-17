from requests import get

"""
Retrieves the current temperature from
another entity from the Home Assistant API
"""

class HaTemperatureClient:
    def __init__(self, host, entity_id, access_token):
        self._entity_id = entity_id
        self._host = host
        self._access_token = access_token


    def current_temperature(self):
        """Gets the current temperature from HA"""

        url = F"http://{self._host}:8123/api/states/{self._entity_id}"
        
        headers = {
            "Authorization": F"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }

        response = get(url, headers=headers)
        
        body = response.json()
        
        if 'state' not in body:
            return None
        
        state = body['state']
        if state == 'unavailable':
            return None

        return float(state)