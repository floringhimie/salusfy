"""
Adds support for the Salus Thermostat units.
"""
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.climate.const import (
    HVACAction,
    HVACMode,
    ClimateEntityFeature,
)
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_ID,
    UnitOfTemperature,
)

CONF_SIMULATOR = 'simulator'

from . import ( ThermostatEntity, WebClient, MockWebClient )

from homeassistant.components.climate import PLATFORM_SCHEMA


from homeassistant.helpers.reload import async_setup_reload_service

__version__ = "0.0.3"


_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Salus Thermostat"

CONF_NAME = "name"



PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_ID): cv.string,
        vol.Optional(CONF_SIMULATOR, default=False): cv.boolean
    }
)


# def setup_platform(hass, config, add_entities, discovery_info=None):
async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    await async_setup_reload_service(hass, DOMAIN, PLATFORMS)
    """Set up the E-Thermostaat platform."""
    name = config.get(CONF_NAME)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    id = config.get(CONF_ID)
    simulator = config.get(CONF_SIMULATOR)

    if (simulator):
        _LOGGER.info('Registering Salus simulator...')
        add_entities(
            [ThermostatEntity(name, MockWebClient())]
        )
    else:
        _LOGGER.info('Registering Salus Thermostat climate entity...')
        web_client = WebClient(username, password, id)

        add_entities(
            [ThermostatEntity(name, web_client)]
        )
