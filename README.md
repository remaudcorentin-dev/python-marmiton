# python-marmiton
##### v0.4.2

Python API to search &amp; get recipes from the 'marmiton.com' website (web crawler, unofficial)  
Useful, efficient and super simple to use.  

###### News (0.4.2) : Minor fix for images list
###### News (0.4.1) : Major update due to changes in the Marmiton website structure - everything working again
###### News (0.3.3) : Bug fixes & code improvements
###### News (0.3.2) : Quick bug fix when h1 class name differ in some pages
###### News (0.3.1) : New fields returned by the 'get' API (see the full list bellow)
###### News (0.2.3) : Package fully up to date on 2018-12-21 on version 0.2.3 according to marmiton website html recent changes

### Installation :
`pip install python-marmiton==0.4.2`

### Requirements :
`python >= 3.4`  
`beautifulsoup4 >= 4.6`  

### API References

##### Marmiton.search returns a list of dictionary like:
- name: name of the recipe.  
- url: url of the detailed recipe on 'marmiton.com'.  
- image: if exists, image of the recipe (url).  
- rate: recipe rate bewteen 0 and 5.  

Note that in version 0.4 the "description" attribute has been removed as it is not available on Marmiton anymore (in search results).

##### Marmiton.get returns a dictionary like:
- name: name of the recipe  
- ingredients: string list of the recipe ingredients (including quantities)  
- steps: string list of each step of the recipe  
- images: list of string, images of the recipe (url).
- cook_time: string, cooking time of the recipe  
- prep_time: string, estimated preparation time of the recipe  
- total_time: string, estimated total time of the recipe (cooking + preparation time)  
- author: string, name of the author of the recipe  
- nb_comments: string, number of comments/rates left by users  
- recipe_quantity: string, quantity indicator the recipie is made for
- budget: string, indicate the category of budget according to the website  
- difficulty: string, indicate the category of difficulty according to the website  
- rate, string: rate of the recipe out of 5  
- author_tip: string, note or tip left by the author  

Notes for version 0.4:
- the "tag" attribute has been removed as it doesn't exists in Marmiton anymore
- the "image" attribute has been replaced by a list of urls in the "images" attribute
- the "people_quantity" has been replace by the "recipe_quantity" attribute, which will include the quantity and the unit (not always number of people now)

### Usage / Example :

```python
from marmiton import Marmiton, RecipeNotFound

# Search :
query_options = {
  "aqt": "boeuf bourguignon",  # Query keywords - separated by a white space
  "dt": "platprincipal",       # Plate type : "entree", "platprincipal", "accompagnement", "amusegueule", "sauce" (optional)
  "exp": 2,                    # Plate price : 1 -> Cheap, 2 -> Medium, 3 -> Kind of expensive (optional)
  "dif": 2,                    # Recipe difficulty : 1 -> Very easy, 2 -> Easy, 3 -> Medium, 4 -> Advanced (optional)
  "veg": 0,                    # Vegetarien only : 0 -> False, 1 -> True (optional)
}
query_result = Marmiton.search(query_options)

# Get :
recipe = query_result[0]
main_recipe_url = recipe['url']

try:
    detailed_recipe = Marmiton.get(main_recipe_url)  # Get the details of the first returned recipe (most relevant in our case)
except RecipeNotFound as e:
    print(f"No recipe found for '{query_options['aqt']}'")
    import sys
    sys.exit(0)

# Display result :
print("## %s\n" % detailed_recipe['name'])  # Name of the recipe
print("Recette par '%s'" % (detailed_recipe['author']))
print("Noté %s/5 par %s personnes." % (detailed_recipe['rate'], detailed_recipe['nb_comments']))
print("Temps de cuisson : %s / Temps de préparation : %s / Temps total : %s." % (detailed_recipe['cook_time'] if detailed_recipe['cook_time'] else 'N/A',detailed_recipe['prep_time'], detailed_recipe['total_time']))
print("Difficulté : '%s'" % detailed_recipe['difficulty'])
print("Budget : '%s'" % detailed_recipe['budget'])

print("\nRecette pour %s :\n" % detailed_recipe['recipe_quantity'])
for ingredient in detailed_recipe['ingredients']:  # List of ingredients
    print("- %s" % ingredient)

print("")

for step in detailed_recipe['steps']:  # List of cooking steps
    print("# %s" % step)

if detailed_recipe['author_tip']:
    print("\nNote de l'auteur :\n%s" % detailed_recipe['author_tip'])
```

### Ongoing features:
- Preparation time, Cooking time, Total time, etc (available on v0.2.2)  
- Multiple images returned for the search / get requests  
- Limit the number of returned query on search  
- More returned data & query options

###### Limitation: This module is provided as it. As Marmiton makes regular updates to their website, this library might stop working temporarily at any time, the time that the code is updated to match the new Marmiton website structure.

##### Important: Please note that the owner of this project does not own any of the returned data, all data are property of MARMITON. This library is shared for free for educational purposes only. The owner declines any responsability of the usage made by the users, please refer to https://www.marmiton.org/sp/aide/conditions-generales-utilisation.html. If you own the website 'www.marmiton.org' and you do not agree with any of the content of this package please send an email to the address bellow.

###### Support / Contact : remaudcorentin.dev@gmail.com
