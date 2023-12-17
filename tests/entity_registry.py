class EntityRegistry:
    def __init__(self):
        self._entities = []
    
    def register(self, list):
        self._entities.extend(list)
    
    @property
    def entities(self):
        return self._entities

    @property
    def first(self):
        return self._entities[0]