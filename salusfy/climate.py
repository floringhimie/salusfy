"""
Adds support for the Salus Thermostat units.
"""
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_ID,
    CONF_ENTITY_ID,
    CONF_ACCESS_TOKEN,
    CONF_HOST
)

CONF_SIMULATOR = 'simulator'
CONF_ENABLE_TEMPERATURE_CLIENT = 'enable_temperature_client'

from . import ( ThermostatEntity, Client, WebClient, HaTemperatureClient )

from . import simulator

from homeassistant.components.climate import PLATFORM_SCHEMA

from homeassistant.helpers.reload import async_setup_reload_service

__version__ = "0.3.0"

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Salus Thermostat"

CONF_NAME = "name"

DOMAIN = "salusfy"
PLATFORMS = ["climate"]

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_ID): cv.string,
        vol.Optional(CONF_SIMULATOR, default=False): cv.boolean,
        vol.Optional(CONF_ENABLE_TEMPERATURE_CLIENT, default=False): cv.boolean,
        vol.Required(CONF_ENTITY_ID): cv.string,
        vol.Required(CONF_ACCESS_TOKEN): cv.string,
        vol.Optional(CONF_HOST, default='localhost'): cv.string
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the E-Thermostat platform."""
    await async_setup_reload_service(hass, DOMAIN, PLATFORMS)

    client = create_client_from(config)
    
    name = config.get(CONF_NAME)
    async_add_entities(
        [ThermostatEntity(name, client)], update_before_add=True
    )


def create_client_from(config):
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    id = config.get(CONF_ID)
    enable_simulator = config.get(CONF_SIMULATOR)
    enable_temperature_client = config.get(CONF_ENABLE_TEMPERATURE_CLIENT)
    entity_id = config.get(CONF_ENTITY_ID)
    host = config.get(CONF_HOST)
    access_token = config.get(CONF_ACCESS_TOKEN)

    if enable_simulator:
        _LOGGER.info('Registering Salus Thermostat client simulator...')

        return Client(simulator.WebClient(), simulator.TemperatureClient())

    web_client = WebClient(username, password, id)
    
    if not enable_temperature_client:
        _LOGGER.info('Registering Salus Thermostat client...')

        return web_client
    
    _LOGGER.info('Registering Salus Thermostat client with Temperature client...')

    ha_client = HaTemperatureClient(host, entity_id, access_token)
    return Client(web_client, ha_client)
