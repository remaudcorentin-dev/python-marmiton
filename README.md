# python-marmiton
##### v0.2.1

Python API to search &amp; get recipes from the 'marmiton.com' website (web crawler, unofficial)  
Useful, efficient and super simple to use.  

### Installation :
`pip install python-marmiton`  

### Requirements :
`python >= 3.4`  
`beautifulsoup4 >= 4.6`  

### API References

##### Marmiton.search return a list of dictionary like :  
- name: name of the recipe.  
- description: short description of the recipe.  
- url: url of the detailed recipe on 'allrecipes.com'.  
- image: if exists, image of the recipe (url).  
- rate: recipe rate bewteen 0 and 5.  

##### Marmiton.get return a dictionary like :  
- name: name of the recipe  
- ingredients: string list of the recipe ingredients (including quantities)  
- steps: string list of each step of the recipe  
- image: if exists, image of the recipe (url).  
- cook_time: string, cooking time of the recipe  
- prep_time: string, estimated preparation time of the recipe  

### Usage / Example :

```python
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
print("## %s :" % detailed_recipe['name'])  # Name of the recipe
print("## Preparation time : %s / Cooking time : %s" % (detailed_recipe['prep_time'], detailed_recipe['cook_time']))  # Cooking & preparation time

for ingredient in detailed_recipe['ingredients']:  # List of ingredients
    print("- %s" % ingredient)

for step in detailed_recipe['steps']:  # List of cooking steps
    print("# %s" % step)
```

### OnGoing features :  
- Preparation time, Cooking time, Total time, etc  
- Multiple images returned for the search / get requests  
- Limit the number of returned query on search  
- More returned data & query options

Related projects :  
- https://github.com/remaudcorentin-dev/python-allrecipes

###### Support / Contact : remaudcorentin.dev@gmail.com

