from marmiton import Marmiton

# Search :
query_options = {
  "aqt": "boeuf bourguignon",      # Query keywords - separated by a white space
  "dt": "platprincipal",      # Plate type : "entree", "platprincipal", "accompagnement", "amusegueule", "sauce" (optional)
  "exp": 2,                   # Plate price : 1 -> Cheap, 2 -> Medium, 3 -> Kind of expensive (optional)
  "dif": 2,                   # Recipe difficulty : 1 -> Very easy, 2 -> Easy, 3 -> Medium, 4 -> Advanced (optional)
  "veg": 0,                   # Vegetarien only : 0 -> False, 1 -> True (optional)
}
query_result = Marmiton.search(query_options)

# Get :
recipes = query_result['props']['pageProps']['searchResults']['hits']
for recipe in recipes:
	print(recipe['title'])
