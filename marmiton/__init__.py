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
                
		articles = soup.findAll("div", {"class": "recipe-card"})


		iterarticles = iter(articles)
		for article in iterarticles:
			data = {}
			try:
				data["name"] = article.find("h4", {"class": "recipe-card__title"}).get_text().strip(' \t\n\r')
				data["description"] = article.find("div", {"class": "recipe-card__description"}).get_text().strip(' \t\n\r')
				data["url"] = article.find("a", {"class": "recipe-card-link"})['href']
				data["rate"] = article.find("span", {"class": "recipe-card__rating__value"}).text.strip(' \t\n\r')
				try:
					data["image"] = article.find('img')['src']
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

		base_url = "http://www.marmiton.org/"
		url = base_url + uri

		html_content = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html_content, 'html.parser')

		main_data = soup.find("div", {"class": "m_content_recette_main"})
		try:
			name = soup.find("h1", {"class", "main-title "}).get_text().strip(' \t\n\r')
		except:
			name = soup.find("h1", {"class", "main-title"}).get_text().strip(' \t\n\r')

		ingredients = [item.text.replace("\n", "").strip() for item in soup.find_all("li", {"class": "recipe-ingredients__list__item"})]

		try:
			tags = list(set([item.text.replace("\n", "").strip() for item in soup.find('ul', {"class": "mrtn-tags-list"}).find_all('li', {"class": "mrtn-tag"})]))
		except:
			tags = []

		recipe_elements = [
			{"name": "author", "query": soup.find('span', {"class": "recipe-author__name"}) },
			{"name": "rate", "query": soup.find("span", {"class": "recipe-reviews-list__review__head__infos__rating__value"}) },
			{"name": "difficulty", "query": soup.find("div", {"class": "recipe-infos__level"}) },
			{"name": "budget", "query": soup.find("div", {"class": "recipe-infos__budget"}) },
			{"name": "prep_time", "query": soup.find("span", {"class": "recipe-infos__timmings__value"}) },
			{"name": "total_time", "query": soup.find("span", {"class": "title-2 recipe-infos__total-time__value"}) },
			{"name": "people_quantity", "query": soup.find("span", {"class": "title-2 recipe-infos__quantity__value"}) },
			{"name": "author_tip", "query": soup.find("div", {"class": "recipe-chief-tip mrtn-recipe-bloc "}).find("p", {"class": "mrtn-recipe-bloc__content"}) if soup.find("div", {"class": "recipe-chief-tip mrtn-recipe-bloc "}) else "" },
		]
		for recipe_element in recipe_elements:
			try:
				data[recipe_element['name']] = Marmiton.__clean_text(recipe_element['query'])
			except:
				data[recipe_element['name']] = ""

		try:
			cook_time = Marmiton.__clean_text(soup.find("div", {"class": "recipe-infos__timmings__cooking"}).find("span"))
		except:
			cook_time = "0"

		try:
			nb_comments = Marmiton.__clean_text(soup.find("span", {"class": "recipe-infos-users__value mrtn-hide-on-print"})).split(" ")[0]
		except:
			nb_comments = ""

		steps = []
		soup_steps = soup.find_all("li", {"class": "recipe-preparation__list__item"})
		for soup_step in soup_steps:
			soup_step.find("h3").decompose()
			steps.append(Marmiton.__clean_text(soup_step))

		image = soup.find("img", {"id": "af-diapo-desktop-0_img"})['src'] if soup.find("img", {"id": "af-diapo-desktop-0_img"}) else ""

		data.update({
			"ingredients": ingredients,
			"steps": steps,
			"name": name,
			"tags": tags,
			"image": image if image else "",
			"nb_comments": nb_comments,
			"cook_time": cook_time
		})

		return data

