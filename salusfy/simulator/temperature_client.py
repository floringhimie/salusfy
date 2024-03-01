"""
Adds support for simulating the Salus Thermostats.
"""


class TemperatureClient:
    def __init__(self):
        pass

    async def current_temperature(self) -> float:
        return 15.9
