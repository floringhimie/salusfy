import logging

from custom_components.salusfy.web_client import (
    WebClient,
    STATE_ON
)

from homeassistant.components.climate.const import (
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE
)

from homeassistant.const import (
    ATTR_TEMPERATURE,
    TEMP_CELSIUS,
)

try:
    from homeassistant.components.climate import ClimateEntity
except ImportError:
    from homeassistant.components.climate import ClimateDevice as ClimateEntity

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE

class ThermostatEntity(ClimateEntity):
    """Representation of a Salus Thermostat device."""

    def __init__(self, name, client):
        """Initialize the thermostat."""
        self._name = name
        self._client = client
        self._state = None
        
        self.update()
    
    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def name(self):
        """Return the name of the thermostat."""
        return self._name
        
    @property
    def unique_id(self) -> str:
        """Return the unique ID for this thermostat."""
        return "_".join([self._name, "climate"])

    @property
    def should_poll(self):
        """Return if polling is required."""
        return True

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return self._client.MIN_TEMP

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return self._client.MAX_TEMP

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._state.current_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._state.target_temperature


    @property
    def hvac_mode(self):
        """Return hvac operation ie. heat, cool mode."""
        try:
            climate_mode = self._state.current_operation_mode
            curr_hvac_mode = HVAC_MODE_OFF
            if climate_mode == STATE_ON:
                curr_hvac_mode = HVAC_MODE_HEAT
            else:
                curr_hvac_mode = HVAC_MODE_OFF
        except KeyError:
            return HVAC_MODE_OFF
        return curr_hvac_mode
        
    @property
    def hvac_modes(self):
        """HVAC modes."""
        return [HVAC_MODE_HEAT, HVAC_MODE_OFF]

    @property
    def hvac_action(self):
        """Return the current running hvac operation."""
        if self._state.status == STATE_ON:
            return CURRENT_HVAC_HEAT
        return CURRENT_HVAC_IDLE
        

    @property
    def preset_mode(self):
        """Return the current preset mode, e.g., home, away, temp."""
        return self._state.status
        
    @property
    def preset_modes(self):
        """Return a list of available preset modes."""
        return SUPPORT_PRESET_MODE
        
        
    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        self._client.set_temperature(temperature)


    def update(self):
        """Get the latest state data."""
        self._state = self._client.get_state()