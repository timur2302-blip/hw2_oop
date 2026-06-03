class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.unit = unit
        self.quantity = quantity

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return self.name == other.name and self.unit == other.unit
        return False

class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        self.ingredients = []
        if ingredients:
            for item in ingredients:
                self.add_ingredient(item)

    def add_ingredient(self, ingredient):
        for item in self.ingredients:
            if item == ingredient:
                item.quantity += ingredient.quantity
                return
        self.ingredients.append(Ingredient(ingredient.name, ingredient.quantity, ingredient.unit))

    @staticmethod
    def is_valid_ratio(ratio):
        if isinstance(ratio, (int, float)) and ratio > 0:
            return True
        return False

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть больше нуля")
        
        new_ingredients = []
        for item in self.ingredients:
            new_ingredients.append(Ingredient(item.name, item.quantity * ratio, item.unit))
        
        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        lines = [self.title]
        for item in self.ingredients:
            lines.append(str(item))
        return "\n".join(lines)

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for item in scaled_recipe.ingredients:
            self._items.append((item, recipe.title))

    def remove_recipe(self, title):
        new_items = []
        for item, recipe_title in self._items:
            if recipe_title != title:
                new_items.append((item, recipe_title))
        self._items = new_items

    def get_list(self):
        grouped = {}
        for item, _ in self._items:
            key = (item.name, item.unit)
            if key in grouped:
                grouped[key] += item.quantity
            else:
                grouped[key] = item.quantity

        result = []
        for (name, unit), quantity in grouped.items():
            result.append(Ingredient(name, quantity, unit))

        result.sort(key=lambda x: x.name)
        return result

    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items.copy() + other._items.copy()
        return new_list

class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio):
        scaled_recipe = super().scale(ratio)
        return DietaryRecipe(scaled_recipe.title, self.diet_type, scaled_recipe.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"