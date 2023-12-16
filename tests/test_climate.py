import pytest

from salusfy import climate
from .config_adapter import ConfigAdapter
from .entity_registry import EntityRegistry

from . import mock_config


def test_entity_is_registered():
    registry = EntityRegistry()
    config_adapter = ConfigAdapter(mock_config)
    climate.setup_platform(None, config_adapter, add_entities=registry.register, discovery_info=None)
    
    assert len(registry.entities) == 1