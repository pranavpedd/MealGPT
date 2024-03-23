from openai import OpenAI

client = OpenAI()

# this is for testing purposes now
def get_ingredients():
    ingredients = []
    while True:
        user_input = input('Ingridients (type done when finished): ')
        
        if user_input.lower() == 'done':
            break

        ingredients.append(user_input)

    cuisine = input('Cuisine: ')
    ingredients_str = ', '.join(ingredients)

    return ingredients_str, cuisine

# main function which generates recipes
def get_recipe(ingredients, cuisine):
    train_msg = "You are a master chef who can make any dish with given ingredients and \
    explain them step by step to anyone - However if there are ingredients that a user does \
    not list which are needed, label those ingredients as 'additional' and list the ones \
    provided as 'provided' and if more spices are required make sure to let the user know \
    this only works assuming they have those spices and provide the average cost of the meal \
    in US dollars"

    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": train_msg},
            {"role": "user", "content": f"Make a dish with the following ingredients: {ingredients} of the {cuisine} cuisine"}
        ]
    )

    return completion.choices[0].message.content.strip()

# runs everything
def main():
    ingredients, cuisine = get_ingredients()
    recipe = get_recipe(ingredients, cuisine)
    print('\n' + recipe)

# make sure this file is run
if __name__ == '__main__':
    main()
