from classes.navigation import Navigation

class NavigationToPath(Navigation):
    """Determines the relative urls of a source directory relative path."""
    def __init__(self, obj, path):
        if (not isinstance(path, str)):
            raise TypeError("The given path must be of type str")
        super().__init__(obj)
        self.path = path

    def get_url_to(self, obj):
        """Returns a url to the given object, relative to self.
        First, searches through own neighbors, then children and lastly the parent.
        Parameters
        ---------
        obj : str
          The source directory relative path to find the url to.
        """
