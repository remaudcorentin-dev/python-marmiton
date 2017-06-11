# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


import urllib.parse
import urllib.request

import re


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
		#ipdb.set_trace()
		main_data = soup.find("div", {"class": "m_resultats_recherche"})
		#ipdb.set_trace()
		articles = soup.findAll("div", {"class": "m_item"})
		#ipdb.set_trace()

		iterarticles = iter(articles)
		for article in iterarticles:
			data = {}
			try:
				data["name"] = article.find("div", {"class": "m_titre_resultat"}).get_text().strip(' \t\n\r')
				data["description"] = article.find("div", {"class": "m_texte_resultat"}).get_text().strip(' \t\n\r')
				data["url"] = article.find("a", href=re.compile('^/recettes/'))['href']
				try:
					data["image"] = article.find("a", href=re.compile('^/recettes/')).find("img")["src"]
				except Exception as e1:
					pass
			except Exception as e2:
				pass
			if data:
				search_data.append(data)

		return search_data

	@staticmethod
	def get(uri):
		"""
		'url' from 'search' method.
		 ex. "/recettes/recette_wraps-de-poulet-et-sauce-au-curry_337319.aspx"
		"""
		base_url = "http://www.marmiton.org/"
		url = base_url + uri

		html_content = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html_content, 'html.parser')

		main_data = soup.find("div", {"class": "m_content_recette_main"})
		name = soup.find("h1", {"class", "m_title fn"}).get_text().strip(' \t\n\r')
		ingredients = [ing.strip(' \t\n\r') for ing in main_data.find("div", {"class": "m_content_recette_ingredients"}).get_text().strip('\r\n\t').split("-")][1:]
		steps = [step.strip(' \t\n\r') for step in main_data.find("div", {"class": "m_content_recette_todo"}).get_text().replace("Préparation de la recette :", "").strip(' \t\n\r').split('.') if step.strip(' \t\n\r')]

		recipe_infos = soup.find("p", {"class": "m_content_recette_info"})
		prep_time = recipe_infos.find("span", {"class": "preptime"}).get_text()
		cook_time = recipe_infos.find("span", {"class": "cooktime"}).get_text()

		data = {"ingredients": ingredients,
				"steps": steps,
				"name": name,
				"prep_time": "%sminutes" % prep_time,
				"cook_time": "%s minutes" % cook_time}

		return data
