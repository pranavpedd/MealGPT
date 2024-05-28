from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # type: ignore
from recipe import get_recipe
from markdown2 import markdown
from weasyprint import HTML
import os

app = Flask(__name__)
cors = CORS(app, origins="*")


@app.route("/generate-recipe", methods=["POST"])
def generate_recipe():
    data = request.json
    ingredients = data.get("ingredients")
    cuisine = data.get("cuisine")
    restriction = data.get("restriction")

    recipe = get_recipe(ingredients, cuisine, restriction)
    if recipe:
        file_name = "recipe.md"
        pdf_file_name = "recipe.pdf"
        extension = "w" if os.path.isfile(file_name) else "x"

        with open(file_name, extension) as f:
            f.write(recipe.choices[0].message.content.strip())

        with open(file_name, "r") as md_file:
            md_content = md_file.read()

        html_content = markdown(md_content)
        HTML(string=html_content).write_pdf(pdf_file_name)
        os.remove(file_name)
        return jsonify({"message": "Recipe was made successfully!"}), 201
    else:
        return jsonify({"message": "Failed to generate recipe"}), 500


@app.route("/download-recipe", methods=["GET"])
def download_recipe():
    root_dir = os.getcwd()
    return send_from_directory(
        directory=root_dir, path="recipe.pdf", as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
