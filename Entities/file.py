class File:
    def __init__(self, file_name, file_content, perimeter, thickness, cutting_speed, cutting_time, nb_folds, height, width):
        self._file_name = file_name
        self._file_content = file_content
        self._perimeter = perimeter
        self._thickness = thickness
        self._cutting_speed = cutting_speed
        self._cutting_time = cutting_time
        self._nb_folds = nb_folds
        self._height = height
        self._width = width 
        
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

    @property
    def cutting_speed(self):
        return self._cutting_speed
    
    @cutting_speed.setter
    def cutting_speed(self, value):
        self._cutting_speed = value

    @property
    def cutting_time(self):
        return self._cutting_time
    
    @cutting_time.setter
    def cutting_time(self, value):
        self._cutting_time = value

    @property
    def nb_folds(self):
        return self._nb_folds
    
    @nb_folds.setter
    def nb_folds(self, value):
        self._nb_folds = value

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
