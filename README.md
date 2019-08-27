# python-marmiton
##### v0.3.2

Python API to search &amp; get recipes from the 'marmiton.com' website (web crawler, unofficial)  
Useful, efficient and super simple to use.  

###### News (0.3.2) : Quick bug fix when h1 class name differ in some pages
###### News (0.3.1) : New fields returned by the 'get' API (see the full list bellow)
###### News (0.2.3) : Package fully up to date on 2018-12-21 on version 0.2.3 according to marmiton website html recent changes

### Installation :
`pip install python-marmiton==0.3.2`  

### Requirements :
`python >= 3.4`  
`beautifulsoup4 >= 4.6`  

### API References

##### Marmiton.search return a list of dictionary like :  
- name: name of the recipe.  
- description: short description of the recipe.  
- url: url of the detailed recipe on 'marmiton.com'.  
- image: if exists, image of the recipe (url).  
- rate: recipe rate bewteen 0 and 5.  

##### Marmiton.get return a dictionary like :  
- name: name of the recipe  
- ingredients: string list of the recipe ingredients (including quantities)  
- steps: string list of each step of the recipe  
- image: if exists, image of the recipe (url).  
- cook_time: string, cooking time of the recipe  
- prep_time: string, estimated preparation time of the recipe  
- (New in 0.3)  
- total_time: string, estimated total time of the recipe (cooking + preparation time)  
- author: string, name of the author of the recipe  
- nb_comments: string, number of comments/rates left by users  
- people_quantity: string, number of people the recipie is made for  
- budget: string, indicate the category of budget according to the website  
- difficulty: string, indicate the category of difficulty according to the website  
- rate, string: rate of the recipe out of 5  
- author_tip: string, note or tip left by the author  
- tags: string list, tags of the recipe  

### Usage / Example :

```python
from marmiton import Marmiton

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

detailed_recipe = Marmiton.get(main_recipe_url)  # Get the details of the first returned recipe (most relevant in our case)

# Display result :
print("## %s\n" % detailed_recipe['name'])  # Name of the recipe
print("Recette par '%s'" % (detailed_recipe['author']))
print("Noté %s/5 par %s personnes." % (detailed_recipe['rate'], detailed_recipe['nb_comments']))
print("Temps de cuisson : %s / Temps de préparation : %s / Temps total : %s." % (detailed_recipe['cook_time'] if detailed_recipe['cook_time'] else 'N/A',detailed_recipe['prep_time'], detailed_recipe['total_time']))
print("Tags : %s" % (", ".join(detailed_recipe['tags'])))
print("Difficulté : '%s'" % detailed_recipe['difficulty'])
print("Budget : '%s'" % detailed_recipe['budget'])

print("\nRecette pour %s personne(s) :\n" % detailed_recipe['people_quantity'])
for ingredient in detailed_recipe['ingredients']:  # List of ingredients
    print("- %s" % ingredient)

print("")

for step in detailed_recipe['steps']:  # List of cooking steps
    print("# %s" % step)

if detailed_recipe['author_tip']:
	print("\nNote de l'auteur :\n%s" % detailed_recipe['author_tip'])
```

### OnGoing features :  
- Preparation time, Cooking time, Total time, etc (available on v0.2.2)  
- Multiple images returned for the search / get requests  
- Limit the number of returned query on search  
- More returned data & query options

Related projects :  
- https://github.com/remaudcorentin-dev/python-allrecipes

###### Support / Contact : remaudcorentin.dev@gmail.com

