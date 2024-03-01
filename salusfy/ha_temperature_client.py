"""Reduces reliance on the Salus API"""
import aiohttp

class HaTemperatureClient:
    """
    Retrieves the current temperature from
    another entity from the Home Assistant API
    """
    def __init__(self, host, entity_id, access_token):
        self._entity_id = entity_id
        self._host = host
        self._access_token = access_token

    async def current_temperature(self) -> float:
        """Gets the current temperature from HA"""

        url = F"http://{self._host}:8123/api/states/{self._entity_id}"

        headers = {
            "Authorization": F"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:

                body = await response.json()

                if 'state' not in body:
                    return None

                state = body['state']
                if state == 'unavailable':
                    return None

                return float(state)
