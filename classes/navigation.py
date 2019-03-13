from classes.category import Category
from classes.asset import Asset
from operator import attrgetter

class Navigation():
    """Determines the relative urls of a navigable object."""
    def __init__(self, obj):
        if (not isinstance(obj, Asset) and not isinstance(obj, Category)):
            raise TypeError("The given object must either be of type Asset or Category (or one of their inheriting classes)")
        self.obj = obj
        self.obj.navigation = self
        self.parent = None # Navigation object
        self.neighbors = []
        self.neighbors_prev = []
        self.neighbors_next = []
        self.get_neighbors()
        self.children = self.get_children()
        print('[Navigation] Acquired %s neighbors for %s' % (str(len(self.neighbors)), self.obj.name))
        print('[Navigation] Acquired %s children for %s' % (str(len(self.children)), self.obj.name))

    def get_neighbors(self):
        """Determines all neighboring Asset/Category objects."""
        neighbors = []
        neighbors_prev = []
        neighbors_next = []
        reached_self = False

        if hasattr(self.obj, 'parent'):
            parent_obj = self.obj.parent
            if isinstance(parent_obj, Category):
                for neighbor in parent_obj.children:
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
                new_child = Navigation(child)
                children.append(new_child)
                new_child.parent = self
            for asset in self.obj.assets:
                new_asset = Navigation(asset)
                children.append(new_asset)
                new_asset.parent = self
        return children
