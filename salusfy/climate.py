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

from . import ( ThermostatEntity, Client, WebClient, MockWebClient, HaTemperatureClient, MockHaTemperatureClient )

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
        vol.Required(CONF_ENTITY_ID): cv.string,
        vol.Required(CONF_ACCESS_TOKEN): cv.string,
        vol.Optional(CONF_HOST, default='localhost'): cv.string
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the E-Thermostat platform."""
    await async_setup_reload_service(hass, DOMAIN, PLATFORMS)

    name = config.get(CONF_NAME)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    id = config.get(CONF_ID)
    simulator = config.get(CONF_SIMULATOR)
    entity_id = config.get(CONF_ENTITY_ID)
    host = config.get(CONF_HOST)
    access_token = config.get(CONF_ACCESS_TOKEN)

    client = None

    if (simulator):
        _LOGGER.info('Registering Salus simulator...')
        client = Client(MockWebClient(), MockHaTemperatureClient())
    else:
        _LOGGER.info('Registering Salus Thermostat climate entity...')
        web_client = WebClient(username, password, id)
        ha_client = HaTemperatureClient(host, entity_id, access_token)
        client = Client(web_client, ha_client)
    
    await async_add_entities(
        [ThermostatEntity(name, client)]
    )