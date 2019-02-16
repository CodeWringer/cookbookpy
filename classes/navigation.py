class Navigation():
    """Base class for navigation objects."""
    def __init__(self, obj):
        self.obj = obj
        self.obj.navigation = self

    def get_url_to(self, obj):
        """Returns a url to the given object, relative to self."""
        return None
