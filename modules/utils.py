'''
Module helpers, should be decorators around functions to provide things like
utf-8 encoding the input.
'''
import requests

def uriSafeQuery(query, trigLen):
	#  format the query
	query = query.encode('utf-8')
	query = str(query)[trigLen:]  # remove trigger from input
	query  = requests.utils.quote(query)  # add %20 for space etc.
	return query

def fmtForSay(html):
    '''replaces things like &lt with < for human to read.'''
    return html.replace('&amp;', '&').replace('&lt;', '<',).replace('&gt;',
     '>').replace('&quot;', '"').replace('&#39;', "'")