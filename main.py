from recipe import get_ingredients
from recipe import get_recipe

def main():
    ingredients, cuisine, restriction = get_ingredients()
    get_recipe(ingredients, cuisine, restriction)


if __name__ == "__main__":
    main()