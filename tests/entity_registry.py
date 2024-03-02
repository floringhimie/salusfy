class EntityRegistry:
    """Registry used for local and test executions."""

    def __init__(self):
        self._entities = []
        self._update_before_add = False

    def register(self, entities, **kwargs):
        """Registers the list of entities."""
        self._update_before_add = kwargs.get('update_before_add')
        self._entities.extend(entities)

    @property
    def entities(self):
        """Returns the list of entries registered during configuration."""
        return self._entities

    @property
    def first(self):
        """Returns the first entity registered."""
        return self._entities[0]

    @property
    def update_before_add(self):
        """
        Determines whether the update_before_add value
        has been set during configuration.
        """
        return self._update_before_add
