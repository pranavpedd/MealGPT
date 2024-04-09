from openai import OpenAI
from markdown2 import markdown
from weasyprint import HTML

import os

client = OpenAI()

# this is for testing purposes now
# ideally this would receive input from the user on the front end
def get_ingredients():
    ingredients = []
    while True:
        ingredient = input("Ingridients (type done when finished): ")

        if ingredient.lower() == "done":
            break

        ingredients.append(ingredient)

    ingredients_str = ", ".join(ingredients)

    cuisine = input("Cuisine: ")

    restrictions = []
    while True:
        restriction = input("Dietary restrictions (done when finished): ")

        if restriction.lower() == "done":
            break

        restrictions.append(restriction)

    restrictions_str = ", ".join(restrictions)

    return ingredients_str, cuisine, restrictions_str


# main function which generates recipes
def get_recipe(ingredients, cuisine, restriction):
    train_msg = "You are a master chef who can make any dish with given ingredients and \
    explain them step by step to anyone with EXTREMELY detailed steps, display the ingredients in a numbered list format, \
    for all the ingredients that were not listed by the user but are needed for the recipe, put '(Additional)' \
    next to them in the list - make sure to include the name of the dish as a title in the recipe at the very \
    top - The user may give you dietary restrictions so make sure you dont include ingredients which would go \
    against these restrictions - It may also be empty in which case proceed with the recipe you were going to give them - \
    Lastly format everything in VERY NEAT AND ORGANIZED markdown so the user can easily read everything when rendered \
    If they have dietary restrictions create a heading and list those out as well in NEAT markdown"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": train_msg},
            {
                "role": "user",
                "content": f"Make a dish with the following ingredients: {ingredients.lower()}. \
                    The cuisine is {cuisine.lower()}. I have these dietary restrictions: {restriction.lower()}",
            },
        ],
    )

    file_name = "recipe.md"
    pdf_file_name = file_name.replace('.md', '.pdf')
    extension = "w" if os.path.isfile(file_name) else "x"
    with open(file_name, extension) as f:
        f.write(completion.choices[0].message.content.strip())

    with open(file_name, 'r') as md_file:
        md_content = md_file.read()

    html_content = markdown(md_content)
    HTML(string=html_content).write_pdf(pdf_file_name)
    os.remove(file_name)

    return True if f else False

