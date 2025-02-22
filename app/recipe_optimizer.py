from app.nutrient_analysis import get_nutrient_data
import app.ai_integration


def optimize_recipe(ingredients, config):
    """
    Optimiza una receta buscando los mejores reemplazos para mejorar su perfil nutricional.

    Args:
        ingredients (list): Lista de ingredientes en la receta original.
        config (dict): Configuración de la API.

    Returns:
        dict: Receta optimizada con mejores sustitutos.
    """
    optimized_recipe = {}
    
    for ingredient in ingredients:
        substitutes = app.ai_integration.find_best_replacement([ingredient], config)
        optimized_recipe[ingredient] = substitutes

    return optimized_recipe

