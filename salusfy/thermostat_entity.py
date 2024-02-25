import logging

from .web_client import (
    STATE_ON,
    STATE_OFF,
    MAX_TEMP,
    MIN_TEMP
)

from .state import State

from homeassistant.components.climate.const import (
    HVACAction,
    HVACMode,
    ClimateEntityFeature
)

from homeassistant.const import (
    ATTR_TEMPERATURE,
    UnitOfTemperature,
)

try:
    from homeassistant.components.climate import ClimateEntity
except ImportError:
    from homeassistant.components.climate import ClimateDevice as ClimateEntity

SUPPORT_FLAGS = ClimateEntityFeature.TARGET_TEMPERATURE

class ThermostatEntity(ClimateEntity):
    """Representation of a Salus Thermostat device."""

    def __init__(self, name, client):
        """Initialize the thermostat."""
        self._name = name
        self._client = client
        self._state = State()

    
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
        return MIN_TEMP

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return MAX_TEMP

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

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
            curr_hvac_mode = HVACMode.OFF
            if climate_mode == STATE_ON:
                curr_hvac_mode = HVACMode.HEAT
            else:
                curr_hvac_mode = HVACMode.OFF
        except KeyError:
            return HVACMode.OFF
        return curr_hvac_mode
        
    @property
    def hvac_modes(self):
        """HVAC modes."""
        return [HVACMode.HEAT, HVACMode.OFF]

    @property
    def hvac_action(self):
        """Return the current running hvac operation."""
        if self._state.status == STATE_ON:
            return HVACAction.HEATING
        return HVACAction.IDLE
        

    @property
    def preset_mode(self):
        """Return the current preset mode, e.g., home, away, temp."""
        return self._state.status
        
    @property
    def preset_modes(self):
        """Return a list of available preset modes."""
        return ClimateEntityFeature.PRESET_MODE
        
        
    async def set_temperature(self, **kwargs):
        """Set new target temperature."""
        
        temperature = kwargs.get(ATTR_TEMPERATURE)
        
        if temperature is None:
            return
        
        await self._client.set_temperature(temperature)
        
        self._state.target_temperature = temperature


    async def set_hvac_mode(self, hvac_mode):
        """Set HVAC mode, via URL commands."""
        
        await self._client.set_hvac_mode(hvac_mode)

        if hvac_mode == HVACMode.OFF:
            self._state.current_operation_mode = STATE_OFF
            self._state.status = STATE_OFF
        elif hvac_mode == HVACMode.HEAT:
            self._state.current_operation_mode = STATE_ON
            self._state.status = STATE_ON
            
    
    async def turn_off(self) -> None:
        await self.set_hvac_mode(HVACAction.OFF)


    async def turn_on(self) -> None:
        await self.set_hvac_mode(HVACAction.HEATING)


    async def async_update(self):
        """Retrieve latest state data."""
        self._state = await self._client.get_state()