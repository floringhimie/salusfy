from requests import get

class HaWebClient:
    def __init__(self, host, entity_id, access_token):
        self._entity_id = entity_id
        self._host = host
        self._access_token = access_token


    def current_temperature(self):
        """Gets the current temperature from """

        url = F"http://{self._host}:8123/api/states/{self._entity_id}"
        
        headers = {
            "Authorization": F"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }

        response = get(url, headers=headers)
        return float(response.json()['state'])