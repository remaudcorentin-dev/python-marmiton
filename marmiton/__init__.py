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
                
		articles = soup.findAll("a", {"class": "recipe-card"})

		iterarticles = iter(articles)
		for article in iterarticles:
			data = {}
			try:
				data["name"] = article.find("h4", {"class": "recipe-card__title"}).get_text().strip(' \t\n\r')
				data["description"] = article.find("div", {"class": "recipe-card__description"}).get_text().strip(' \t\n\r')
				data["url"] = article['href']
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
		name = soup.find("h1", {"class", "main-title "}).get_text().strip(' \t\n\r')

		ingredients = [item.text.replace("\n", "").strip() for item in soup.find_all("li", {"class": "recipe-ingredients__list__item"})]

		steps = []
		soup_steps = soup.find_all("li", {"class": "recipe-preparation__list__item"})
		for soup_step in soup_steps:
			soup_step.find("h3").decompose()
			steps.append(soup_step.text.replace("\n", "").replace("\t", "").strip())

		prep_time = "0"
		cook_time = "0"

		try:
			prep_time = soup.find("span", {"class": "recipe-infos__timmings__value"}).text.replace("\n", "").replace("\t", "").strip()
		except:
			pass

		try:
			cook_time = soup.find("div", {"class": "recipe-infos__timmings__cooking"}).find("span").text.replace("\n", "").replace("\t", "").strip()
		except:
			pass

		image = soup.find("img", {"id": "af-diapo-desktop-0_img"})['src'] if soup.find("img", {"id": "af-diapo-desktop-0_img"}) else ""

		data = {"ingredients": ingredients,
				"steps": steps,
				"name": name,
				"image": image if image else "",
				"prep_time": prep_time,
				"cook_time": cook_time}

		return data

