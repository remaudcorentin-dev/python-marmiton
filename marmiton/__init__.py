# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

import re


class RecipeNotFound(Exception):
	pass


class Marmiton(object):

	@staticmethod
	def search(query_dict):
		"""
		Search recipes parsing the returned html data.
		Options:
		'aqt': string of keywords separated by a white space  (query search)
		Optional options :
		'dt': "entree" | "platprincipal" | "accompagnement" | "amusegueule" | "sauce"  (plate type)
		'exp': 1 | 2 | 3  (plate expense 1: cheap, 3: expensive)
		'dif': 1 | 2 | 3 | 4  (recipe difficultie 1: easy, 4: advanced)
		'veg': 0 | 1  (vegetarien only: 1)
		'rct': 0 | 1  (without cook: 1)
		'sort': "markdesc" (rate) | "popularitydesc" (popularity) | "" (empty for relevance)
		"""
		base_url = "http://www.marmiton.org/recettes/recherche.aspx?"
		query_url = urllib.parse.urlencode(query_dict)

		url = base_url + query_url

		html_content = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html_content, 'html.parser')

		search_data = []

		articles = soup.findAll("a", {"class": "MRTN__sc-1gofnyi-2 gACiYG"})

		iterarticles = iter(articles)
		for article in iterarticles:
			data = {}
			try:
				data["name"] = article.find("h4", {"class": "MRTN__sc-30rwkm-0 dJvfhM"}).get_text().strip(' \t\n\r')
				data["url"] = article['href']
				data["rate"] = article.find("span", {"class": "SHRD__sc-10plygc-0 jHwZwD"}).text.strip(' \t\n\r')
				try:
					data["image"] = article.find('img')['data-src']
				except Exception as e1:
					pass
			except Exception as e2:
				pass
			if data:
				search_data.append(data)

		return search_data

	@staticmethod
	def __clean_text(element):
		return element.text.replace("\n", "").strip()

	@staticmethod
	def get(uri):
		"""
		'url' from 'search' method.
		 ex. "/recettes/recette_wraps-de-poulet-et-sauce-au-curry_337319.aspx"
		"""
		data = {}

		base_url = "http://www.marmiton.org"
		url = base_url + ("" if uri.startswith("/") else "/") + uri

		try:
			html_content = urllib.request.urlopen(url).read()
		except urllib.error.HTTPError as e:
			raise RecipeNotFound if e.code == 404 else e

		soup = BeautifulSoup(html_content, 'html.parser')

		main_data = soup.find("div", {"class": "SHRD__sc-juz8gd-1 kOwNOA"})
		
		name = soup.find("h1", {"class", "SHRD__sc-10plygc-0 itJBWW"}).get_text().strip(' \t\n\r')

		ingredients = []
		soup_ingredients = soup.find_all('div', {'class':'MuiGrid-root MuiGrid-item MuiGrid-grid-xs-3 MuiGrid-grid-sm-3'})
		for soup_ingredients in soup_ingredients:
			try:
			    ingredients.append(element.find('span', {'class':'RCP__sc-8cqrvd-3 cDbUWZ'}).get_text())
			except:
			    ingredients.append(element.find('span', {'class':'RCP__sc-8cqrvd-3 itCXhd'}).get_text())

		recipe_elements = [
			{"name": "author", "query": soup.find('span', {"class": "RCP__sc-ox3jb6-5 fwQMuu"})},
			{"name": "rate","query": soup.find("span", {"class": "SHRD__sc-10plygc-0 jHwZwD"})},
			{"name": "difficulty", "query": soup.find("div", {"class": "RCP__sc-1qnswg8-1 iDYkZP"})},
			{"name": "budget", "query": soup.find("p", {"class": "RCP__sc-1qnswg8-1 iDYkZP"})},
			{"name": "prep_time", "query": soup.find("span", {"class": "SHRD__sc-10plygc-0 bzAHrL"})},
			{"name": "total_time", "query": soup.find("p", {"class": "RCP__sc-1qnswg8-1 iDYkZP"})},
			{"name": "people_quantity", "query": soup.find("span", {"class": "SHRD__sc-w4kph7-4 hYSrSW"})},
			{"name": "author_tip", "query": soup.find("div", {"class": "RCP__sc-ox3jb6-8 eWzWSo"})},
		]
		for recipe_element in recipe_elements:
			try:
				data[recipe_element['name']] = Marmiton.__clean_text(recipe_element['query'])
			except:
				data[recipe_element['name']] = ""

		try:
			cook_time = Marmiton.__clean_text(soup.find("span", {"class": "SHRD__sc-10plygc-0 bzAHrL"})
		except:
			cook_time = "0"

		try:
			nb_comments = Marmiton.__clean_text(soup.find("span", {"class": "SHRD__sc-10plygc-0 cAYPwA"})).split(" ")[0]
		except:
			nb_comments = ""

		steps = []
		soup_steps = soup.find_all('p', {'class':'RCP__sc-1wtzf9a-3 jFIVDw'})
		for soup_step in soup_steps:
			steps.append(Marmiton.__clean_text(soup_step))

		data.update({
			"ingredients": ingredients,
			"steps": steps,
			"name": name,
			"tags": tags,
			"nb_comments": nb_comments,
			"cook_time": cook_time
		})

		return data

