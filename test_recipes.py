import pytest
from main import Ingredient, Recipe, ShoppingList, DietaryRecipe

def test_ingredient_init():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_str():
    ing = Ingredient("Мука", 500, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq():
    ing1 = Ingredient("Мука", 500, "г")
    ing2 = Ingredient("Мука", 200, "г")
    ing3 = Ingredient("Сахар", 500, "г")
    ing4 = Ingredient("Мука", 500, "кг")
    
    assert ing1 == ing2
    assert ing1 != ing3
    assert ing1 != ing4

def test_recipe_init():
    ing1 = Ingredient("Мука", 500, "г")
    rec = Recipe("Тесто", [ing1])
    assert rec.title == "Тесто"
    assert len(rec.ingredients) == 1

def test_recipe_add_ingredient():
    rec = Recipe("Тесто")
    rec.add_ingredient(Ingredient("Мука", 500, "г"))
    rec.add_ingredient(Ingredient("Мука", 200, "г"))
    assert len(rec.ingredients) == 1
    assert rec.ingredients[0].quantity == 700.0

def test_recipe_scale():
    rec = Recipe("Тесто", [Ingredient("Мука", 500, "г")])
    scaled = rec.scale(2)
    assert scaled != rec
    assert scaled.ingredients[0].quantity == 1000.0
    
    with pytest.raises(ValueError):
        rec.scale(-1)

def test_recipe_len():
    rec = Recipe("Тесто", [Ingredient("Мука", 500, "г"), Ingredient("Сахар", 200, "г")])
    assert len(rec) == 2

def test_shopping_list_add_recipe():
    sl = ShoppingList()
    rec = Recipe("Тесто", [Ingredient("Мука", 500, "г")])
    sl.add_recipe(rec, 2)
    assert len(sl._items) == 1
    assert sl._items[0][0].quantity == 1000.0
    
    with pytest.raises(ValueError):
        sl.add_recipe(rec, 0)

def test_shopping_list_remove_recipe():
    sl = ShoppingList()
    rec = Recipe("Тесто", [Ingredient("Мука", 500, "г")])
    sl.add_recipe(rec, 1)
    sl.remove_recipe("Тесто")
    assert len(sl._items) == 0

def test_shopping_list_remove_nonexistent_recipe():
    sl = ShoppingList()
    rec = Recipe("Тесто", [Ingredient("Мука", 500, "г")])
    sl.add_recipe(rec, 1)
    sl.remove_recipe("Суп")
    assert len(sl._items) == 1

def test_shopping_list_get_list():
    sl = ShoppingList()
    rec1 = Recipe("Тесто", [Ingredient("Мука", 500, "г")])
    rec2 = Recipe("Блинчики", [Ingredient("Мука", 200, "г"), Ingredient("Молоко", 1, "л")])
    sl.add_recipe(rec1, 1)
    sl.add_recipe(rec2, 1)
    res = sl.get_list()
    assert len(res) == 2
    assert res[0].name == "Молоко"
    assert res[1].name == "Мука"
    assert res[1].quantity == 700.0

def test_shopping_list_add():
    sl1 = ShoppingList()
    sl2 = ShoppingList()
    rec1 = Recipe("Тесто", [Ingredient("Мука", 500, "г")])
    rec2 = Recipe("Вода", [Ingredient("Вода", 1, "л")])
    sl1.add_recipe(rec1, 1)
    sl2.add_recipe(rec2, 1)
    sl3 = sl1 + sl2
    assert len(sl3._items) == 2
    assert len(sl1._items) == 1
    assert len(sl2._items) == 1 