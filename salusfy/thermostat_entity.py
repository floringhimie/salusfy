from homeassistant.components.climate.const import (
    HVACAction,
    HVACMode,
    ClimateEntityFeature,
    PRESET_NONE,
)

from homeassistant.const import (
    ATTR_TEMPERATURE,
    UnitOfTemperature,
)

from .web_client import (
    MAX_TEMP,
    MIN_TEMP
)

try:
    from homeassistant.components.climate import ClimateEntity
except ImportError:
    from homeassistant.components.climate import ClimateDevice as ClimateEntity


class ThermostatEntity(ClimateEntity):
    """Representation of a Salus Thermostat device."""

    def __init__(self, name, client):
        """Initialize the thermostat."""
        self._name = name
        self._client = client

        self._state = None

        self._enable_turn_on_off_backwards_compatibility = False

    @property
    def supported_features(self) -> ClimateEntityFeature:
        """Return the list of supported features."""
        return (ClimateEntityFeature.TARGET_TEMPERATURE
                | ClimateEntityFeature.TURN_ON
                | ClimateEntityFeature.TURN_OFF)

    @property
    def name(self) -> str:
        """Return the name of the thermostat."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique ID for this thermostat."""
        return "_".join([self._name, "climate"])

    @property
    def should_poll(self) -> bool:
        """Return if polling is required."""
        return True

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature."""
        return MIN_TEMP

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature."""
        return MAX_TEMP

    @property
    def temperature_unit(self) -> UnitOfTemperature:
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self) -> float:
        """Return the current temperature."""
        return self._state.current_temperature

    @property
    def target_temperature(self) -> float:
        """Return the temperature we try to reach."""
        return self._state.target_temperature

    @property
    def hvac_mode(self) -> HVACMode:
        """Return hvac operation ie. heat, cool mode."""

        return self._state.mode

    @property
    def hvac_modes(self) -> list[HVACMode]:
        """HVAC modes."""
        return [HVACMode.HEAT, HVACMode.OFF]

    @property
    def hvac_action(self) -> HVACAction:
        """Return the current running hvac operation."""
        return self._state.action

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode, e.g., home, away, temp."""
        return PRESET_NONE

    @property
    def preset_modes(self) -> list[str]:
        """Return a list of available preset modes."""
        return [PRESET_NONE]

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""

        temperature = kwargs.get(ATTR_TEMPERATURE)

        if temperature is None:
            return

        await self._client.set_temperature(temperature)

        self._state.target_temperature = temperature

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set HVAC mode, via URL commands."""

        await self._client.set_hvac_mode(hvac_mode)

        self._state.mode = hvac_mode

    async def async_turn_off(self) -> None:
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_turn_on(self) -> None:
        await self.async_set_hvac_mode(HVACMode.HEAT)

    async def async_update(self) -> None:
        """Retrieve latest state data."""
        self._state = await self._client.get_state()
