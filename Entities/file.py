
class File:
    def __init__(self, file_name, perimeter ,thickness):
        self.file_name = file_name
        self.perimeter = perimeter
        self.thickness = thickness
        
    @property
    def file_name(self):
        return self._file_name
    
    @file_name.setter
    def file_name(self, value):
        self._file_name = value
    
    @property
    def perimeter(self):
        return self._perimeter
    
    @perimeter.setter
    def perimeter(self, value):
        self._perimeter = value

    @property
    def thickness(self):
        return self._thickness
    
    @thickness.setter
    def thickness(self, value):
        self._thickness = value