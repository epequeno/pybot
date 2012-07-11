'''
Functions for Google services http://www.google.com/
'''
import requests
import urllib
import utils

NUM_RESULTS = 3  # number of results to return should not be > 3
RESPONSE_TITLE_LENGTH = 40

def makeUri(variation):
	return 'http://ajax.googleapis.com/ajax/services/search/%s?v=1.0&safe=off&q=' % variation

def search(query, variation='web', trigLen=3):
	'''search returns a generator object with the first NUM_RESULTS results.
	optional params uri and trigLen are set to defaut 'web' and 3'''
	
	query = utils.uriSafeQuery(query, trigLen)
	response = requests.get(makeUri(variation) + query)

	if response.status_code != 200:
		yield "HTTP response != 200"
		return

	for i in range(0, NUM_RESULTS):
		results = response.json['responseData']['results']
		if len(results) == 0:
			yield "Nothing found!"
			break
		title = utils.fmtForSay(results[i]['titleNoFormatting'])
		url = urllib.unquote(results[i]['url'])
		answer = ('%s (%s)' % (title[:RESPONSE_TITLE_LENGTH], url))
		yield answer

def news(query):
	'''news returns a generator object with the first NUM_RESULTS results
	calls search() passing optional params'''
	return search(query, variation='news', trigLen=6)

def images(query):
	'''images returns a generator object with the first NUM_RESULTS results
	calls search() passing optional params'''
	return search(query, variation='images', trigLen=5)

def books(query):
	'''books returns a generator object with the first NUM_RESULTS results
	calls search() passing optional params'''
	return search(query, variation='books', trigLen=7)