from classes.asset_content import AssetContent
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
        self.servings = super().get_section('Servings')
        self.ingredients = super().get_section('Ingredients')
        self.utensils = super().get_section('Utensils')
        self.preparation = super().get_section('Preparation')
        self.cooking = super().get_section('Cooking')

    def render(self, generator, dest_dir):
        """Renders and writes out this asset."""
        # Render self.
        super().render(generator, dest_dir)

    def get_rendered(self, generator):
        """Returns an html representation of this asset."""
        categories_toc = self.parent.get_rendered_for_toc()
        title = self.title
        titleimage = None # TODO

        categories = self.get_categories(generator)
        neighbor_previous = self.get_neighbor_prev()
        neighbor_next = self.get_neighbor_next()

        ingredients = '\n'.join(self.ingredients)
        utensils = '\n'.join(self.utensils)
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
