class EntityRegistry:
    def __init__(self):
        self._entities = []
    
    async def register(self, list):
        print('xxxxxxxxxxxxxxx')
        self._entities.extend(list)
    
    @property
    def entities(self):
        return self._entities

    @property
    def first(self):
        return self._entities[0]