from classes.navigation import Navigation

class NavigationForPath(Navigation):
    """Determines the relative urls of a source directory relative path."""
    def __init__(self, obj, path, source_content_dir):
        if (not isinstance(path, str)):
            raise TypeError("The given path must be of type str")
        super().__init__(obj)
        self.path = path
        self.source_content_dir = source_content_dir

    def get_url_to(self, obj):
        """Returns a url to the given object, relative to self.
        First, searches through own neighbors, then children and lastly the parent.
        Parameters
        ---------
        obj : str
          The source directory relative path to find the url to.
          e.g.: theme/main.css
        """
        rel_path_self = self.obj.path[len(self.source_content_dir):]
        split_self = rel_path_self.replace('\\', '/').split('/')

        rel_path_goal = self.path.replace('\\', '/')

        url = ''
        for split in split_self:
            url += '**/'

        if rel_path_goal.startswith('/'):
            rel_path_goal = rel_path_goal[1:]

        return url + '/' + rel_path_goal
