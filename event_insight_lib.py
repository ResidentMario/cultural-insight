'''event-insight.py
    Library defining the methods making up the event insight tool.'''

# A Python SDK is currently being written to handle these tasks, and will hopefully come out in the next week or so.
# Once that is done this code will be 

import json
import os
import requests
from time import strftime, gmtime

'''Finds the credentials file describing the token that's needed to access Watson/Bluemix services.
Returns a {url, username, password} token if successful, fataly aborts if not.
Handing off authorization in this manner keeps account credentials secure.
Takes one optional argument, the name of the JSON file in which the credentials are stored. `credentials.json` is the default.
This internal method is a component of the externally-facing `generateToken()` method.'''
def importCredentials(filename='credentials.json'):
	if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
		data = json.load(open(filename))['concept_insights'][0]['credentials']
		return data
	else:
		raise IOError('FATAL ERROR: This API requires a Bluemix/Watson credentials token to work. Did you forget to define one? For more information refer to:\n\nhttps://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/getting_started/gs-credentials.shtml')

'''Uses the credentials returned by a call to `importCredentials()` to generate the Base64 token that IBM uses for API authorization.
Takes the name of the credentials file as an optional argument, to be passed to `importCredentials()`; defaults to `credentails.json` if none is provided.
This method will need to be called as the first step of the execution of any script wishing to reference the API.
Note that tokens expire after an hour of use (or non-use).'''
def generateToken(filename='credentials.json', tokenfile='token.json'):
	credentials = importCredentials(filename)
	r = requests.get("https://gateway.watsonplatform.net/authorization/api/v2/token\?url=https://stream.watsonplatform.net/concept-insights/api", auth=(credentials['username'], credentials['password']))
	if r.status_code == requests.codes.ok:
		f = open(tokenfile, 'w')
		f.write(json.dumps({'token': r.text, 'time': gmtime()}, indent=4))
		return r.text
	else:
		raise RuntimeError('FATAL ERROR: Could not resolve a Bluemix/Watson API token using the given credentials. Are your account credentials correct?')

'''Given the text to be analyzed and a previous generated access token this method returns the result of an API call to the `annotate_text` Watson method.
This method forms the core of this library's functionality.
This method accepts one optional parameter: `content_type`. This defaults to `text/plain`, which expects plaintext input. `text/html` is the alternative option.'''
def annotateText(text, token, content_type = 'text/plain'):
	base_url='https://watson-api-explorer.mybluemix.net/concept-insights/api/v2/graphs/wikipedia/en-20120601/annotate_text'
	headers = {'X-Watson-Authorization-Token': token, 'Content-Type': content_type, 'Accept': 'application/json'}
	dat = text.encode(encoding='UTF-8', errors='ignore')
	print(dat)
	r = requests.post(base_url, headers=headers, data=dat)
	print(r.text)
	return json.loads(r.text)

'''Helper function for saving a file.'''
def saveFile(content, filename):
	f = open(filename, 'w')
	f.write(json.dumps(content, indent=4))
	f.close()