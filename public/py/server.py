from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, Response
import imdb
import json
from lxml import html
from mechanize import Browser
import os.path
import random
import requests
from socket import *
import sys
import urllib2
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '9eca7af565a64946adc7626c44935eb5'
SESSION_ID = "<SESSION ID, UNIQUE FOR EACH USER>"
GENRE_COUNT=0
GENRES=""
"""
jd=i.search_person('Johnny depp')[0]
i.update(jd, 'all')
print jd.summary()
# movie_list is a list of Movie objects, with only attributes like 'title'
# and 'year' defined.
movie_list = i.search_movie('the passion')
print movie_list
# the first movie in the list.
first_match = movie_list[0]
# only basic information like the title will be printed.
print first_match.summary()
# update the information for this movie.
i.update(first_match)
# a lot of information will be printed!
print first_match.summary()
# retrieve trivia information and print it.
i.update(first_match, 'trivia')
print m['trivia']
# retrieve both 'quotes' and 'goofs' information (with a list or tuple)
i.update(m, ['quotes', 'goofs'])
print m['quotes']
print m['goofs']
# retrieve every available information.
i.update(m, 'all')
"""
def peopleCount(imdbID):
	return len(imdbID.split(','))
def genres():
	global GENRES
	url="http://www.imdb.com/search/title?genres="+GENRES+"&explore=languages&languages=en&view=simple"
	page = requests.get(url)
	tree = html.fromstring(page.text)
	soup = BeautifulSoup(page.text, 'html.parser')
	movies_name = soup.findAll("span",{"class":"lister-item-header"})
	retstr=""
	retstr="Here are top 10 movies in "+GENRES+" : <br> "
	for movie_name in range(10):
		retstr=retstr+movies_name[movie_name].find('a').get_text()+" <br>"
	"""print ("Do you want to add another genres to refine your search?")
				print ("1. Yes")
				print ("2. No")
				choice=str(raw_input())
				print choice
				if choice=='1':
					new_genre=str(raw_input())
					genre=genre+','+new_genre
				else: 
					#ask for movie number here
					break"""
	return retstr
def actors():
	print "Enter the actor's name : "
	aname=str(raw_input())
	i = imdb.IMDb()
	person=i.search_person(aname)[0]
	imdbID=i.get_imdbURL(person).split('/')[-2]
	url="http://www.imdb.com/filmosearch?explore=title_type&role="+imdbID+"&ref_=filmo_vw_smp&sort=user_rating,desc&mode=simple&page=1&title_type=movie&job_type=actor"
	while True:
		print url
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		movies_name = soup.findAll("span",{"class":"lister-item-header"})
		if len(movies_name)==0 and peopleCount(imdbID)==1:
			url="http://www.imdb.com/filmosearch?explore=title_type&role="+imdbID+"&ref_=filmo_vw_smp&sort=user_rating,desc&mode=simple&page=1&title_type=movie&job_type=actress"
			page = requests.get(url)	
			soup = BeautifulSoup(page.text, 'html.parser')
			movies_name = soup.findAll("span",{"class":"lister-item-header"})
			if len(movies_name)==0:
				print "Sorry no data found for",aname
		else:
			page = requests.get(url)	
			soup = BeautifulSoup(page.text, 'html.parser')
			movies_name = soup.findAll("span",{"class":"lister-item-header"})
			if len(movies_name)==0:
				print "Sorry no data found for",aname
		rating = soup.findAll("div",{"class":"col-imdb-rating"})
		print ("Here are top 10 feature presentations of "+aname+" :")
		for movie_name in range((10 if len(movies_name)>=10 else len(movies_name))):
			s=""
			if peopleCount(imdbID)>1:
				rating_movie_index=movie_name
			else:
				rating_movie_index=movie_name+1
			year = movies_name[movie_name].findAll("span",{"class":"lister-item-year text-muted unbold"})
			for heads in movies_name[movie_name].findAll('a'):
				s+=heads.get_text()+" "
			print s,year[-1].get_text(),"\t",(rating[rating_movie_index].find('strong') if rating[rating_movie_index].find('strong')!=None else rating[rating_movie_index].find('span')).get_text().strip()
		print ("Do you want to add another actor to refine your search?")
		print ("1. Yes")
		print ("2. No")
		choice=str(raw_input())
		print choice
		if choice=='1':
			new_aname=str(raw_input())
			new_person=i.search_person(new_aname)[0]
			new_imdbID=i.get_imdbURL(new_person).split('/')[-2]
			imdbID+=','+new_imdbID
			aname+=','+new_aname
			url="http://www.imdb.com/search/title?roles="+imdbID+"&title_type=feature,tv_episode,video,tv_movie,tv_special,mini_series,documentary,game,short&sort=user_rating,desc&view=simple"
		else: 
			#ask for movie number here
				break

def apiaifunc(query):
	ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
	request = ai.text_request()
	request.session_id = SESSION_ID
	request.query = query
	response = json.loads(request.getresponse().read())
	return (response['result']['fulfillment']['speech'])

app = Flask(__name__)
@app.route('/reset', methods=['GET'])
def resetEverything():
	global GENRE_COUNT, GENRES
	print "here"
	GENRE_COUNT=0
	GENRES=""

@app.route('/receiver', methods = ['GET'])
def worker():
	global GENRE_COUNT, GENRES
	# read json + reply
	ret_data = {"value": request.args.get('query')}
	response = apiaifunc(ret_data['value']).split(':')
	category,value=response[0],response[1]
	if category=='genre':
		print "here1"
		GENRE_COUNT=GENRE_COUNT+1
		print "here"
		if len(GENRES)==0:
			print "1"
			GENRES=value
		else:
			print "2"
			GENRES=GENRES+','+value
		if GENRE_COUNT==1:
			print "3"
			movie_list="Current genre count is too less for any personalized result. Why don't you give me one more genre?"
		elif GENRE_COUNT>=2:
			print "4"
			movie_list=genres()
	print "5"
	return movie_list
if __name__ == '__main__':
	# run!
	GENRE_COUNT=0
	app.run(host='127.0.0.1', port=80)


	"""print ("Hi, how do you want to search for a movie?")
				print ("1. Genres")
				print ("2. Actor")
				print ("3. Director")
				print ("4. Movie Name")
				print ("5. Top Rated")
				print ("6. Time period - old, fairly new, latest")
				print ("7. Oscar winning")
				print ("8. Oscar nominated")
				print ("9. Company")
				print ("Choose an input:")
				choice=str(raw_input())
				if choice=='1': genres()
				elif choice=='2': actors()"""