from classes.asset import Asset

class AssetRecipe(Asset):
    """Represents a recipe."""
    def __init__(self, file_path):
        super().__init__(file_path)
        self.servings = ''
        self.ingredients = []
        self.utensils = []
        self.preparation = []
        self.cooking = []
        self.get_recipe()

    def get_recipe(self):
        """Analyzes the file found via the given absolute path."""
        self.servings = super().get_section(_('Servings'))
        self.ingredients = super().get_section(_('Ingredients'))
        self.utensils = super().get_section(_('Utensils'))
        self.preparation = super().get_section(_('Preparation'))
        self.cooking = super().get_section(_('Cooking'))
