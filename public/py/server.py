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
from netflix import *
from random import randint


CLIENT_ACCESS_TOKEN = '9eca7af565a64946adc7626c44935eb5'
SESSION_ID = "<SESSION ID, UNIQUE FOR EACH USER>"
GENRES=""
ACTORS=""
URL=""
MORE=0
CURRENT_MOVIE=""
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
def find_between( s, first, last ):
    try:
    	print "s",s,first,last
        start = s.index(first.split()[0]) + len(first)
        print "start",start
        end = s.index( last.split()[0], start )
        print "end",end
        return s[start:end]
    except ValueError:
        return ""
def peopleCount(imdbID):
	return len(imdbID.split(','))
# def genres():
# 	global GENRES,URL
# 	URL+="&genres="+GENRES
# 	page = requests.get(url)
# 	tree = html.fromstring(page.text)
# 	soup = BeautifulSoup(page.text, 'html.parser')
# 	movies_name = soup.findAll("span",{"class":"lister-item-header"})
# 	retstr=""
# 	retstr="Here are top 3 movies in "+GENRES+" : <br> "
# 	for movie_name in range(3):
# 		retstr=retstr+movies_name[movie_name].find('a').get_text()+" <br>"
# 	"""print ("Do you want to add another genres to refine your search?")
# 				print ("1. Yes")
# 				print ("2. No")
# 				choice=str(raw_input())
# 				print choice
# 				if choice=='1':
# 					new_genre=str(raw_input())
# 					genre=genre+','+new_genre
# 				else: 
# 					#ask for movie number here
# 					break"""
# 	return retstr
# def actors(actor):
# 	global URL
# 	print "actors"
# 	retstr=""
# 	s=""
# 	i = imdb.IMDb()
# 	actorscount=len(actor.split(','))
# 	print actorscount
# 	if actorscount==1:
# 		person=i.search_person(actor)[0]
# 		imdbID=i.get_imdbURL(person).split('/')[-2]
# 		tempUrl=URL+"&role="+imdbID+"&sort=user_rating,desc&title_type=movie"
# 		print "tempUrl",tempUrl
# 		page = requests.get(tempUrl)
# 		soup = BeautifulSoup(page.text, 'html.parser')
# 		movies_name = soup.findAll("span",{"class":"lister-item-header"})
# 		if len(movies_name)==0:
# 			return "Sorry no data found for "+actor+"<br>"
# 		rating = soup.findAll("div",{"class":"col-imdb-rating"})
# 		retstr+="Here are top 3 feature presentations of "+actor+" :<br>"
# 		for movie_name in range((3 if len(movies_name)>=3 else len(movies_name))):
# 			print movies_name[movie_name]
# 			year = movies_name[movie_name].findAll("span",{"class":"lister-item-year text-muted unbold"})
# 			print "1"
# 			for heads in movies_name[movie_name].findAll('a'):
# 				print "2"
# 				s=heads.get_text()+" "
# 			print "s",s
# 			retstr+=s+" "+year[-1].get_text()+"&emsp;"+(rating[movie_name].find('strong') if rating[movie_name].find('strong')!=None else rating[movie_name].find('span')).get_text().strip()+"<br>"
# 			print retstr
# 		return retstr+"<br>"
# 	else:
# 		print "1"
# 		actorlist=actor.split(',')
# 		print actorlist
# 		imdbID=[i.get_imdbURL(y).split('/')[-2] for y in [i.search_person(x)[0] for x in actorlist]]
# 		print "imdbID",imdbID
# 		imdbID=','.join(imdbID)
# 		print "imdbID2",imdbID
# 		tempUrl=URL+"&role="+imdbID+"&sort=user_rating,desc&title_type=movie"
# 		print "tempUrl",tempUrl
# 		page = requests.get(tempUrl)
# 		soup = BeautifulSoup(page.text, 'html.parser')
# 		movies_name = soup.findAll("span",{"class":"lister-item-header"})
# 		if len(movies_name)==0:
# 			return "Sorry no data found for "+actor+"<br>"
# 		rating = soup.findAll("div",{"class":"col-imdb-rating"})
# 		retstr+="Here are top 3 feature presentations of "+actor+" :<br>"
# 		for movie_name in range((3 if len(movies_name)>=3 else len(movies_name))):
# 			print movies_name[movie_name]
# 			year = movies_name[movie_name].findAll("span",{"class":"lister-item-year text-muted unbold"})
# 			print "1"
# 			for heads in movies_name[movie_name].findAll('a'):
# 				print "2"
# 				s=heads.get_text()+" "
# 			print "s",s
# 			retstr+=s+" "+year[-1].get_text()+"&emsp;"+(rating[movie_name].find('strong') if rating[movie_name].find('strong')!=None else rating[movie_name].find('span')).get_text().strip()+"<br>"
# 			print retstr
# 		return retstr+"<br>"

def getCasts(cast_list):
	cast_name=[]
	i = imdb.IMDb()
	for cast in cast_list:
		person=i.search_person(cast)[0]
		imdbID=i.get_imdbURL(person).split('/')[-2]
		cast_name.append(imdbID)
	return cast_name
def getTopMoviesNames(start, end):
	global URL, CURRENT_MOVIE
	print "URL",URL
	page = requests.get(URL)
	tree = html.fromstring(page.text)
	soup = BeautifulSoup(page.text, 'html.parser')
	header = soup.findAll("h1",{"class":"header"})
	movies_name = soup.findAll("td",{"class":"titleColumn"})
	if movies_name:
		print len(movies_name),start
		if len(movies_name)>start:
			noOfMovies=3 if len(movies_name)-start>=3 else len(movies_name)-start
			print "noOfMovies",noOfMovies
			retstr=""
			rating = soup.findAll("td",{"class":"ratingColumn imdbRating"})
			if start==0:
				retstr="Here are top "+str(noOfMovies)+" "+header[0].get_text()+" : <br> "
			else:
				retstr="Here are next "+str(noOfMovies)+" "+header[0].get_text()+" : <br> "
			for movie_name in range(start, start+noOfMovies):
				year = movies_name[movie_name].findAll("span",{"class":"secondaryInfo"})
				for heads in movies_name[movie_name].findAll('a'):
					s=heads.get_text()+" "
					print "noOfMovies1",noOfMovies
					if noOfMovies==1:
						CURRENT_MOVIE=heads.get_text()
					else:
						CURRENT_MOVIE=""
				retstr+=s+"  released in the year "+year[-1].get_text().replace('(','').replace(')','')+" with imdB rating of "+(rating[movie_name].find('strong') if rating[movie_name].find('strong')!=None else rating[movie_name].find('span')).get_text().strip()+"<br>"
				print "1"
				#retstr+=find_movie(s)+"<br><br>"
				#print "retstr"+retstr
			return retstr+"<br>"
		else:
			return "No more movies left of this combination."
	else:
		return "No more movies left of this combination."
def getMoviesNames(start, end):
	global URL, CURRENT_MOVIE
	print "URL",URL
	page = requests.get(URL)
	tree = html.fromstring(page.text)
	soup = BeautifulSoup(page.text, 'html.parser')
	header = soup.findAll("h1",{"class":"header"})
	movies_name = soup.findAll("span",{"class":"lister-item-header"})
	if movies_name:
		print len(movies_name),start
		if len(movies_name)>start:
			noOfMovies=3 if len(movies_name)-start>=3 else len(movies_name)-start
			print "noOfMovies",noOfMovies
			retstr=""
			rating = soup.findAll("div",{"class":"col-imdb-rating"})
			if start==0:
				retstr="Here are top "+str(noOfMovies)+" "+header[0].get_text()+" : <br> "
			else:
				retstr="Here are next "+str(noOfMovies)+" "+header[0].get_text()+" : <br> "
			for movie_name in range(start, start+noOfMovies):
				year = movies_name[movie_name].findAll("span",{"class":"lister-item-year text-muted unbold"})
				for heads in movies_name[movie_name].findAll('a'):
					s=heads.get_text()+" "
					print "noOfMovies1",noOfMovies
					if noOfMovies==1:
						CURRENT_MOVIE=heads.get_text()
					else:
						CURRENT_MOVIE=""
				retstr+=s+"  released in the year "+year[-1].get_text().replace('(','').replace(')','')+" with imdB rating of "+(rating[movie_name].find('strong') if rating[movie_name].find('strong')!=None else rating[movie_name].find('span')).get_text().strip()+"<br>"
				print "1"
				#retstr+=find_movie(s)+"<br><br>"
				#print "retstr"+retstr
			return retstr+"<br>"
		else:
			return "No more movies left of this combination."
	else:
		return "No more movies left of this combination."
def apiaifunc(query):
	ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
	req = ai.text_request()
	req.session_id = SESSION_ID
	req.query = query
	resp = json.loads(req.getresponse().read())
	return (resp['result']['fulfillment']['speech'])

app = Flask(__name__)
@app.route('/reset', methods=['GET'])
def resetEverything():
	global SESSION_ID
	SESSION_ID = randint(0, 10000)

@app.route('/receiver', methods = ['GET'])
def worker():
	global GENRE_COUNT, GENRES, ACTOR_COUNT, ACTORS, URL, MORE, CURRENT_MOVIE
	try:
		im = imdb.IMDb()
		orOrAnd = ""

		# read json + reply
		ret_data = {"value": request.args.get('query')}
		response = apiaifunc(ret_data['value']).split(':')
		print response,ret_data
		if response[0]=='param':
			URL="http://www.imdb.com/search/title?explore=languages&languages=en&view=simple&sort=user_rating,desc&num_votes=10000,&title_type=feature"
			MORE=0
			for i in range(1, len(response), 2):
				category,value=response[i],response[i+1]
				if category=='Genre':
					value=value.split('and')
					genres=','.join(value)
					URL+="&genres="+genres
					print URL
				elif category=='Director':
					value=value.split('and')
					directors=getCasts(value)
					print "directors",directors
					if len(directors)>1 and (value[0] in ret_data['value']):
						orOrAnd = find_between(ret_data['value'], value[0], value[1])
					else:
						orOrAnd = "AND"
					print orOrAnd
					movie_list=""
					if 'OR' in orOrAnd.upper():
						for j in range(len(directors)):
							tempURL=URL+"&role="+directors[j]+"&page=1&job_type=director"
							tempURL_swap=URL
							URL=tempURL
							movie_list+=getMoviesNames(0,3)+"<br><br>"
							URL=tempURL_swap
						return movie_list
					else:# 'AND' in orOrAnd.upper():
						directors=','.join(directors)
					URL+="&role="+directors+"&page=1&job_type=director"
					print URL
				elif category=='Actor':
					value=value.split('and')
					actors=getCasts(value)
					print "actors",actors, len(actors)
					if len(actors)>1 and (value[0] in ret_data['value']):
						orOrAnd = find_between(ret_data['value'], value[0], value[1])
					else:
						orOrAnd = "AND"
					print orOrAnd
					movie_list=""
					if 'OR' in orOrAnd.upper():
						for j in range(len(actors)):
							tempURL=URL+"&role="+actors[j]+"&page=1&job_type=actor"
							tempURL_swap=URL
							URL=tempURL
							movie_list+=getMoviesNames(0,3)+"<br><br>"
							URL=tempURL_swap
						return movie_list
					else:# 'AND' in orOrAnd.upper():
						actors=','.join(actors)
						print actors
					URL+="&role="+actors+"&page=1&job_type=actor"
					print URL
			movie_list=getMoviesNames(0,3)
			return movie_list
		elif response[0]=='more_about':
			print "CURRENT_MOVIE", CURRENT_MOVIE
			if CURRENT_MOVIE=="" and response[1]=='this':
				return "Can you please specify which movie?"
			else:
				movie_name=response[1] if response[1]!='this' else CURRENT_MOVIE
				print movie_name

				s_result = im.search_movie(movie_name)
				the_unt = s_result[0]
				name = '+'.join(str(the_unt).split())
				print "movie_name",the_unt
				ytURL="https://www.youtube.com/results?search_query="+name.replace('&','and')+"+trailer"
				print ytURL
				
				imdbURL=im.get_imdbURL(the_unt)
				page = requests.get(imdbURL)
				tree = html.fromstring(page.text)
				soup = BeautifulSoup(page.text, 'html.parser')
				summary = soup.findAll("div",{"class":"summary_text"})[0].get_text()
				print imdbURL
				
				page = requests.get(ytURL)
				tree = html.fromstring(page.text)
				soup = BeautifulSoup(page.text, 'html.parser')
				trailer_link = "https://www.youtube.com"+soup.findAll("div",{"class":"yt-lockup-thumbnail contains-addto"})[0].find('a')['href']
				print "trailer_link",trailer_link
				
				netflix_link = find_movie(str(the_unt))+"<br><br>"
				print "netflix_link",netflix_link
				
				im.update(the_unt, 'trivia')
				trivia = the_unt['trivia'][0]
				print "trivia",trivia
				
				if netflix_link!="Sorry! Movie not on Netflix.<br><br>":
					return "INFO:SUMMARY=> "+summary+"<br>TRIVIA=> "+trivia+"<br>TRAILER=><a href=\""+trailer_link+"\">"+trailer_link+"</a><br>NETFLIX=><a href=\""+netflix_link+"\">"+netflix_link
				else:
					return "INFO:SUMMARY=> "+summary+"<br>TRIVIA=> "+trivia+"<br>TRAILER=><a href=\""+trailer_link+"\">"+trailer_link+"</a><br>NETFLIX=>"+netflix_link
		elif response[0]=='param?more':
			MORE+=1
			print URL
			if URL=='http://www.imdb.com/chart/top':
				movie_list=getTopMoviesNames(MORE*3,(MORE+1)*3)	
			else:
				movie_list=getMoviesNames(MORE*3,(MORE+1)*3)
			return movie_list
		elif response[0]=='imdb':
			print response[0]
			URL="http://www.imdb.com/chart/top"
			#tempURL_swap=URL
			#URL=tempURL
			movie_list=getTopMoviesNames(0,3)
			#URL=tempURL_swap
			return movie_list
		elif response[0]=='Here are some commands you could try':
			return response[0]+response[1]
		else:
			return response[0]
	except:
		return "Sorry! I'm not trained for that, but I'm still learning. Try \'help me\'"
if __name__ == '__main__':
	# run!
	GENRE_COUNT=0
	ACTOR_COUNT=0
	app.run(host='127.0.0.1', port=80)