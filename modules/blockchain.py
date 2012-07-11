'''
Functions for http://blockchain.info services
'''
import requests
import utils

BASE_URI = 'http://blockchain.info/q/'

def makeRequest(stat):
	return requests.get(BASE_URI + stat).content

def stats():
	currentDifficulty = float(makeRequest('getdifficulty'))
	blockCount = makeRequest('getblockcount')
	unconfirmedCount = makeRequest('unconfirmedcount')
	hashRate = float(makeRequest('hashrate'))
	price24hr = float(makeRequest('24hrprice'))
	transactions24hr = makeRequest('24hrtransactioncount')
	return ('[Difficulty %.2f] [blockcount %s] [Unconfirmed transactions %s] [Hashrate %.2fGH/s] [24hr Price %.2f] [24hr Transactions %s]' 
		% (currentDifficulty, blockCount, unconfirmedCount, hashRate, price24hr, transactions24hr))
