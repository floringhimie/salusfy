"""Exercises the Salus client as if it was run through Home Assistant"""

# To run this script to test the component:
# 1 Copy config.sample.py to config.py
# 2 Replace the username/password/deviceid (don't worry, this file will be ignored by git)
# 3 Run with `python run.py`

import asyncio
import logging

import argparse

from homeassistant.components.climate.const import HVACMode

from salusfy import climate
from tests.test_climate import MockHass
from tests.config_adapter import ConfigAdapter
from tests.entity_registry import EntityRegistry


import config

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


async def main(set_temp: bool) -> None:
    """Exercises the Salus client"""

    registry = EntityRegistry()
    config_adapter = ConfigAdapter(config)

    await climate.async_setup_platform(
        MockHass(), config_adapter, async_add_entities=registry.register, discovery_info=None)

    thermostat = registry.first

    await thermostat.async_update()
    await thermostat.async_update()

    if set_temp:
        await thermostat.async_set_hvac_mode(HVACMode.HEAT)
        await thermostat.async_set_temperature(temperature=9.8)

    print("Current: " + str(thermostat.current_temperature))
    print("Target: " + str(thermostat.target_temperature))
    print("HVAC Action: " + thermostat.hvac_action)
    print("HVAC Mode: " + thermostat.hvac_mode)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Salus Client Simulator")
    parser.add_argument("--set_temp", default=False, required=False,
                        help="Determines whether to set the temp",
                        type=bool)
    args = parser.parse_args()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(args.set_temp))
