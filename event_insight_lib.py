'''event-insight.py
    This library provides a way to access IBM Watson Bluemix services via tokenization.
    This is actually not the recommended way of handling access!
    A Pythonic API is currently in stalled development by the Bluemix team, which would make this module redundant.
    But, for now, this is what I use.'''

import json
import os
import requests
from time import strftime, gmtime

'''Finds the credentials file describing the token that's needed to access Watson/Bluemix services.
Returns a {url, username, password} dictionary token if successful, fataly aborts if not.
Handing off authorization in this manner keeps account credentials secure.
Takes one optional argument, the name of the JSON file in which the credentials are stored. `credentials.json` is the default.
This internal method is a component of the externally-facing `generateToken()` method.'''
def importCredentials(filename='concept_insight_credentials.json'):
	if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
		data = json.load(open(filename))['credentials']
		return data
	else:
		raise IOError('FATAL ERROR: This API requires a Bluemix/Watson credentials token to work. Did you forget to define one?' +
			'For more information refer to:\n\nhttps://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/getting_started/gs-credentials.shtml')

'''Uses the credentials returned by a call to `importCredentials()` to generate the Base64 token that IBM uses for API authorization.
	Takes the name of the credentials file as an optional argument, to be passed to `importCredentials()`; defaults to `credentails.json` if none is provided.
	This method is a submethod of the primary-use `getToken()` method.
	See also `validateToken()`, below.'''
def generateToken(filename='concept_insight_credentials.json', tokenfile='token.json'):
	credentials = importCredentials(filename)
	r = requests.get("https://gateway.watsonplatform.net/authorization/api/v2/token\?url=https://stream.watsonplatform.net/concept-insights/api",
		auth=(credentials['username'], credentials['password']))
	if r.status_code == requests.codes.ok:
		f = open(tokenfile, 'w')
		f.write(json.dumps({'token': r.text, 'time': gmtime()}, indent=4))
		return r.text
	else:
		raise RuntimeError('FATAL ERROR: Could not resolve a Bluemix/Watson API token using the given credentials. Are your account credentials correct?')

'''The generateToken() method creates a JSON file with both a token and a time parameter.
	This methods checks if the token file is still valid. Tokens live for an hour, so if the token was generated less than an hour ago
	it should work. In that case the additional overhead of regenerating the token is not necessary!
	This method is a submethod of the primary-use `getToken()` method.
	See also `generateToken()`, above.'''
def validateToken(tokenfile='token.json'):
	if tokenfile in [f for f in os.listdir('.') if os.path.isfile(f)]:
		# The timestamp is in UTC. The timestamp is in the format [year, month, day, hour, minute, second, ..., ..., ...]
		# Generated via `gmtime()` in `generateToken()`. See https://docs.python.org/2/library/time.html#time.struct_time
		# In our case it's simplest to compare the hour parameter and make sure we haven't incremented into the next hour yet.
		# Time is not fun, especially in Python, so nothing more complex so far.
		timestamp = json.load(open(tokenfile))['time']
		hourstamp = timestamp[3]
		if hourstamp - gmtime()[3] == 0:
			return True
		else:
			return False
	else:
		return False

'''This is the primary-use access method meant to be used throughout the application.
	Implements `validateToken()` and `generateToken()` submethods, above.
	If a token exists that was created within the current hour, it is still valid, reused, and returned (fast).
	If a token exists but has expired, or does not exist at all, one is created and returned (requires networking, slower).'''
def getToken(tokenfile='token.json'):
	if validateToken():
		return json.load(open(tokenfile))['token']
	else:
		return generateToken()

'''Given the text to be analyzed and a previous generated access token this method returns the result of an API call to the `annotate_text` Watson method.
This method forms the core of this library's functionality.
This method accepts one optional parameter: `content_type`. This defaults to `text/plain`, which expects plaintext input.
`text/html` is the alternative option.'''
def annotateText(text, token, content_type = 'text/plain'):
	base_url='https://watson-api-explorer.mybluemix.net/concept-insights/api/v2/graphs/wikipedia/en-20120601/annotate_text'
	headers = {'X-Watson-Authorization-Token': token, 'Content-Type': content_type, 'Accept': 'application/json'}
	dat = text.encode(encoding='UTF-8', errors='ignore')
	r = requests.post(base_url, headers=headers, data=dat)
	return json.loads(r.text)