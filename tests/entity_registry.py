class EntityRegistry:
    def __init__(self):
        self._entities = []
        self._update_before_add = False
    
    
    def register(self, list, **kwargs):
        self._update_before_add = kwargs.get('update_before_add')
        self._entities.extend(list)
    

    @property
    def entities(self):
        return self._entities


    @property
    def first(self):
        return self._entities[0]
    

    @property
    def update_before_add(self):
        return self._update_before_add