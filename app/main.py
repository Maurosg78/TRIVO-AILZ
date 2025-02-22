from flask import Flask, request, jsonify
import json
from nutrient_analysis import analyze_nutrients
from recipe_optimizer import optimize_recipe

app = Flask(__name__)

# Cargar configuraciones
with open('config/usda_config.json') as f:
    usda_config = json.load(f)

@app.route('/')
def home():
    return "Bienvenido a TRIVO AI - Optimización de recetas"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    ingredients = data.get('ingredients')
    if not ingredients:
        return jsonify({"error": "No se proporcionaron ingredientes."}), 400
    analysis_result = analyze_nutrients(ingredients, usda_config)
    return jsonify(analysis_result)

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    recipe = data.get('recipe')
    if not recipe:
        return jsonify({"error": "No se proporcionó una receta."}), 400
    optimized_recipe = optimize_recipe(recipe, usda_config)
    return jsonify(optimized_recipe)

if __name__ == '__main__':
    app.run(debug=True)