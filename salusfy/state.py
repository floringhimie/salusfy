class State:
    """The state of the thermostat."""
    def __init__(self):
        self.current_temperature = None
        self.target_temperature = None
        self.frost = None
        self.status = None
        self.current_operation_mode = None