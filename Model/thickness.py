class Thickness:
    def __init__(self, thickness):
        self.thickness = thickness
        
    @property
    def thickness(self):
        return self._thickness
    
    @thickness.setter
    def thickness(self, value):
        self._thickness = value