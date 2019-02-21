from classes.asset_content import AssetContent
from utility.url import get_url
import markdown

class AssetRecipe(AssetContent):
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

    def render(self, generator, dest_dir):
        """Renders and writes out this asset."""
        # Render self.
        super().render(generator, dest_dir)

    def get_rendered(self, generator):
        """Returns an html representation of this asset."""
        categories_toc = self.parent.get_rendered_for_toc()
        title = self.title
        titleimage = None # TODO

        categories = []
        for category in generator.root_category.children:
            categories.append({ 'name': category.name,
                                'url': get_url(self.path,
                                               category.file_path) })

        neighbor_previous = None
        neighbor_next = None
        if len(self.navigation.neighbors_prev) > 0:
            neighbor = self.navigation.neighbors_prev[0]
            neighbor_previous = {
                'title': neighbor.title,
                'url': get_url(self.path,
                               neighbor.path)
            }
        if len(self.navigation.neighbors_next) > 0:
            neighbor = self.navigation.neighbors_next[0]
            neighbor_next = {
                'title': neighbor.title,
                'url': get_url(self.path,
                               neighbor.path)
            }

        ingredients = [_('Ingredient | Amount | Notes'), '-- | -- | --']
        ingredients = '\n'.join(ingredients + self.ingredients)

        utensils = [_('Utensil | Notes'), '-- | --']
        utensils = '\n'.join(utensils + self.utensils)

        preparation = '\n'.join(self.preparation)
        cooking = '\n'.join(self.cooking)

        ingredients = markdown.markdown(ingredients, ['extra'])
        utensils = markdown.markdown(utensils, ['extra'])
        preparation = markdown.markdown(preparation, ['extra'])
        cooking = markdown.markdown(cooking, ['extra'])
        servings = self.servings[0]
        # see_also = TODO
        # prepimages = TODO

        rendered = generator.templates['template_recipe'].render(
            language = generator.language,
            styles = generator.get_style_urls(self),
            categories_toc = categories_toc,
            categories = categories,
            category = { 'name': self.parent.name },
            title = title,
            titleimage = titleimage,
            neighbor_previous = neighbor_previous,
            neighbor_next = neighbor_next,
            ingredients_header = _('Ingredients'),
            utensils_header = _('Utensils'),
            preparation_header = _('Preparation'),
            cooking_header = _('Cooking'),
            for_servings = _('Ingredients for %s servings:' % (servings)),
            ingredients = ingredients,
            utensils = utensils,
            preparation = preparation,
            cooking = cooking,
            # prepimages = prepimages,
            # see_also = see_also
        )
        return rendered
