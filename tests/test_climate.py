import pytest

from salusfy import climate
from .config_adapter import ConfigAdapter
from .entity_registry import EntityRegistry

from . import mock_config

# pylint: disable=missing-function-docstring


class MockHass:
    """Mocks the HASS for use during unit tests."""
    @property
    def services(self):
        return self

    def has_service(self,
                    domain,  # pylint: disable=unused-argument
                    service,  # pylint: disable=unused-argument
                    ):
        return False

    def async_register(self, domain, service, admin_handler, schema):
        pass


@pytest.mark.asyncio
async def setup_climate_platform():
    registry = EntityRegistry()
    config_adapter = ConfigAdapter(mock_config)
    await climate.async_setup_platform(MockHass(),
                                       config_adapter,
                                       async_add_entities=registry.register,
                                       discovery_info=None)
    return registry


@pytest.mark.asyncio
async def test_entity_is_registered():
    registry = await setup_climate_platform()

    assert len(registry.entities) == 1


@pytest.mark.asyncio
async def test_entity_is_updated_before_added():
    registry = await setup_climate_platform()

    assert registry.update_before_add


@pytest.mark.asyncio
async def test_entity_returns_mock_temperature():
    registry = await setup_climate_platform()

    thermostat = registry.first

    await thermostat.async_update()

    assert thermostat.current_temperature == 15.9


@pytest.mark.asyncio
async def test_entity_returns_mock_target_temperature():
    registry = await setup_climate_platform()

    thermostat = registry.first

    await thermostat.async_update()

    assert thermostat.target_temperature == 20.1
