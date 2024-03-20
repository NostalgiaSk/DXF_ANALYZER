class File:
    def __init__(self, file_name, file_content, perimeter, thickness):
        self._file_name = file_name
        self._file_content = file_content
        self._perimeter = perimeter
        self._thickness = thickness
        
    @property
    def file_name(self):
        return self._file_name
    
    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def file_content(self):
        return self._file_content
    
    @file_content.setter
    def file_content(self, value):
        self._file_content = value
    
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
