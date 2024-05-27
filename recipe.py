from openai import OpenAI
from markdown2 import markdown
from weasyprint import HTML

from training_message import message

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
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": message
            },

            {
                "role": "user",
                "content": f"Make a dish with the following ingredients: {ingredients.lower()}. \
                    The cuisine is {cuisine.lower()}. Tailor to these dietary restrictions: {restriction.lower()}",
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

