'''
Functions for bitcoincharts:
http://bitcoincharts.com/t/markets.json
'''
import requests
import re

NUM_CHAR_TO_SEARCH = 20
RESPONSE = requests.get('http://bitcoincharts.com/t/markets.json')
if RESPONSE.status_code == 200:
	TICKER = RESPONSE.json
	SYMBOLS = [str(market['symbol']) for market in TICKER]
else:
	SYMBOLS = []

def getData(symbol):
	marketIndex = SYMBOLS.index(symbol)
	data = ['symbol', 'low', 'ask', 'bid', 'high', 'volume']
	
	for i in range(0, len(data)):
		value = TICKER[marketIndex][data[i]]
		if value == None:
			data[i] = 0.0
		else:
			data[i] = value
	return data

def marketData(msg):
	'''Looks in the first NUM_CHAR_TO_SEARCH of msg for a market
	symbol. It could be	extended to search the whole message but
	that's wasteful. Intended use: !btc <market symbol> padding 
	is for new market symbols defaults to mtgoxUSD'''
	if len(SYMBOLS) == 0:
		return "err: http response code != 200"

	regex = re.compile(" *")
	if regex.match(msg[:NUM_CHAR_TO_SEARCH]):
		data = getData('mtgoxUSD')

	for symbol in SYMBOLS:
		if symbol in msg[:NUM_CHAR_TO_SEARCH]:
			data = getData(symbol)
	
	return ('%s lo{ask/bid}hi\x0314 %.4s\x03 {\x034 %.4s \x03/\x033 %.4s \x03}\x0314 %.4s\x03 vol: %.2f' % 
		(data[0], data[1], data[2], data[3], data[4], data[5]))