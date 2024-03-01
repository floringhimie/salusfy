"""Exposes state of the thermostat."""

import dataclasses

@dataclasses.dataclass
class State:
    """The state of the thermostat."""
    current_temperature = None
    target_temperature = None
    frost = None
    action = None
    mode = None
