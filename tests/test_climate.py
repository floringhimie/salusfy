import pytest

from salusfy import climate
from .config_adapter import ConfigAdapter
from .entity_registry import EntityRegistry

from . import mock_config


def setup_climate_platform():
    registry = EntityRegistry()
    config_adapter = ConfigAdapter(mock_config)
    climate.setup_platform(None, config_adapter, add_entities=registry.register, discovery_info=None)
    return registry


def test_entity_is_registered():
    registry = setup_climate_platform()
    
    assert len(registry.entities) == 1


def test_entity_returns_mock_temperature():
    registry = setup_climate_platform()

    thermostat = registry.first
    
    assert thermostat.current_temperature == 15.9


def test_entity_returns_mock_target_temperature():
    registry = setup_climate_platform()

    thermostat = registry.first
    
    assert thermostat.target_temperature == 20.1