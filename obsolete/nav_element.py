class NavigationElement:
    """Model class to represent a navigation element"""
    def __init__(self, url, name, children=None):
        self.url = url
        self.name = name
        if children == None:
            self.children = []
        else:
            self.children = children

    def __str__(self):
        return self.url + ', ' + self.name