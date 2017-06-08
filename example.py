
from marmiton import Marmiton
 
# Search :
query_options = {
  "aqt": "poulet curry",      # Query keywords - separated by a white space
  "sort": "rate",             # Sorting options : "markdesc" (rate) | "popularitydesc" (popularity) | "" (empty for relevance, optional)
  "dt": "platprincipal",      # Plate type : "entree", "platprincipal", "accompagnement", "amusegueule", "sauce" (optional)
  "exp": 3,                   # Plate price : 1 -> Cheap, 2 -> Medium, 3 -> Kind of expensive (optional)
  "dif": 2,                   # Recipe difficulty : 1 -> Very easy, 2 -> Easy, 3 -> Medium, 4 -> Advanced (optional)
  "veg": 0,                   # Vegetarien only : 0 -> False, 1 -> True (optional)
  "rct": 0,                   # Without cooking : 0 -> False, 1 -> True (optional)
}
query_result = Marmiton.search(query_options)

# Get :
main_recipe_url = query_result[0]['url']
detailed_recipe = Marmiton.get(main_recipe_url)  # Get the details of the first returned recipe (most relevant in our case)

# Display result :
print("## %s :" % query_result[0]['name'])  # Name of the recipe

for ingredient in detailed_recipe['ingredients']:  # List of ingredients
    print("- %s" % ingredient)

for step in detailed_recipe['steps']:  # List of cooking steps
    print("# %s" % step)
