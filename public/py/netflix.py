from splinter import Browser
from time import sleep

def find_movie_name(browser, movie_name):
	url = "https://www.justwatch.com/us/search?q="+movie_name
	print url
	browser.visit(url)
	try:
		movies_name = browser.find_by_css('.main-content__list-element__content.col-xs-8.col-sm-10').find_by_tag('div').find_by_tag('a').find_by_tag('span')
		print movies_name
		for name in movies_name:
			print name
			if name.html.upper()==movie_name.upper():
				return True
		return False
	except:
		return False
def get_providers(browser, movie_name):
	url = "https://www.justwatch.com/us/search?q="+movie_name
	browser.visit(url)
	try:
		providers = browser.find_by_css('.price-comparison__grid__row__icon')
		link_divs = browser.find_by_css('.presentation-type.price-comparison__grid__row__element__icon').find_by_tag('a')
		titles = []
		links = []
		for provider in providers:
			title = provider['title']
			titles.append(title)
		for link_div in link_divs:
			link = link_div['href']
			links.append(link)
		print "titles, links", titles, links
		return titles,links
	except:
		return None, None
def find_netflix(providers):
	return 'Netflix' in providers
def get_index(providers):
	return providers.index('Netflix')
def get_netflix_link(s):
	first="?r="
	last="&"
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return ""
def find_movie(movie_name):
	print "movie_name1",movie_name 
	with Browser('chrome') as browser:
		print "inside"
		movie_exists=find_movie_name(browser, movie_name)
		print movie_exists
		if movie_exists:
			providers,links = get_providers(browser, movie_name)
			if find_netflix(providers):
				index=get_index(providers)
				if len(links)>index:
					return get_netflix_link(links[index]).replace('%2F','/').replace('%3A',':')
				else:
					return "Sorry! Movie not on Netflix."
			else:
				return "Sorry! Movie not on Netflix."
		else:
			return "Sorry! Movie not on Netflix."
	return "Sorry! Movie not on Netflix."