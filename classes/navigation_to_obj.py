from classes.category import Category
from classes.navigation import Navigation
from classes.asset import Asset
from operator import attrgetter

class NavigationToObj(Navigation):
    """Determines the relative urls of a navigable object."""
    def __init__(self, obj):
        if (not isinstance(obj, Asset) and not isinstance(obj, Category)):
            raise TypeError("The given object must either be of type Asset or Category (or one of their inheriting classes)")
        super().__init__(obj)
        self.parent = None # NavigationToObj object
        self.neighbors = []
        self.neighbors_prev = []
        self.neighbors_next = []
        self.get_neighbors()
        self.children = self.get_children()
        print('[NavigationToObj] Acquired %s neighbors for %s' % (str(len(self.neighbors)), self.obj.name))
        print('[NavigationToObj] Acquired %s children for %s' % (str(len(self.children)), self.obj.name))

    def get_neighbors(self):
        """Determines all neighboring Asset/Category objects."""
        parentObj = self.obj.parent
        neighbors = []
        neighbors_prev = []
        neighbors_next = []
        reached_self = False
        if isinstance(parentObj, Category):
            for neighbor in parentObj.children:
                if neighbor == self.obj:
                    reached_self = True
                    continue
                elif reached_self:
                    neighbors_next.append(neighbor)
                else:
                    neighbors_prev.append(neighbor)
                neighbors.append(neighbor)
        self.neighbors_prev = sorted(neighbors_prev,
                                     key=attrgetter('name'),
                                     reverse=True)
        self.neighbors_next = sorted(neighbors_next,
                                     key=attrgetter('name'))
        self.neighbors = sorted(neighbors, key=attrgetter('name'))

    def get_children(self):
        """Creates Navigation objects and returns them as a list."""
        children = []
        if isinstance(self.obj, Category):
            for child in self.obj.children:
                children.append(NavigationToObj(child))
            for child in self.obj.assets:
                children.append(NavigationToObj(child))
        return children

    def get_url_to(self, obj):
        """Returns a url to the given object, relative to self.
        First, searches through own neighbors, then children and lastly the parent.
        Parameters
        ---------
        obj : Asset or Category
          The object to find the url to.
        """
        if (not isinstance(obj, Asset) and not isinstance(obj, Category)):
            raise TypeError("The given object must either be of type Asset or Category (or one of their inheriting classes)")
        # Test neighbors.
        for neighbor in self.neighbors:
            if neighbor == obj:
                return '/../%s' % (neighbor.name)
        # Test children.
        for child in self.children:
            if child == obj:
                return '/%s' % (child.name)
            else:
                childUrl = child.navigation.get_url_to(obj)
                if childUrl != None:
                    return '/%s%s' % (child.name, childUrl)
        # Test parent.
        if self.parent == obj:
            return '/..'
        else:
            parentUrl = self.parent.navigation.get_url_to(obj)
            if parentUrl != None:
                return '/..%s' % (parentUrl)
        return None

