"""backend.py
	This library defines the backend used by the application webservice, `app.py`.
	The Watson/Core methods contained here are wrappers of `event_insight_lib.py` methods."""

# Redistributables.
import json
import os
import random
import itertools
import requests

# My own libraries.
import event_insight_lib
# from user import User

#############
# INTERFACE #
#############
# This section contains all of the backend methods servicing the user interface layer of the webservice.

def emailAlreadyInUse(new_email, filename='accounts.json'):
	"""Checks if an email is already in use. Returns True if it is, False if not."""
	# Open the accounts file.
	if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
		list_of_users = json.load(open(filename))['accounts']
	# Check to see if the selected email appears in the list.
	for existing_user in list_of_users:
		if existing_user['email'] == new_email:
			return True
	return False

def authenticateUser(email, password, filename='accounts.json'):
	"""Authenticates a user's email-password combination."""
	if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
		list_of_users = json.load(open(filename))['accounts']
	# Check to see if the selected email appears in the list.
	for existing_user in list_of_users:
		if existing_user['email'] == email and existing_user['password'] == password:
			return True
	return False

def initializeSecretString():
	"""
	Imports the secret string used by some of the Flask plug-ins for security purposes.
	The secret string is be a simple randomly generated numerical, defined at runtime.
	"""
	return random.random()

#################
# END INTERFACE #
#################

###############
# WATSON/CORE #
###############
# This section contains the systemic core of the application---its interface with the IBM Watson Concept Insights service.
# These are high-level methods which wrap low-level methods contained in the event_insight_lib library.
# Some terminology:
# A "Concept Node" is a Wikipedia pagename which is associated with an "Concept Model" when run through the Concept Insights service.
# The "Concept Model" is the model for a particular user's conceptual preferences.
# eg. {'Modern art': 0.67, 'History of music': 0.89}
# These are associated with the .model property of an ObjectModel object, which stores the model and some metadata about the model:
# its maturity and the email of the associated account.
# ConceptModel objects are read from and written to `accounts.json` for permanent storage.

def getToken(tokenfile='token.json'):
	"""
	This is the primary-use access method meant to be used throughout the application.
	Path-wrapper for the getToken() method in event_insight_lib.py.
	"""
	return event_insight_lib.getToken(tokenfile)

def fetchConceptsForUserConcept(institution, token, cutoff=0.5):
	"""
	Given a user-defined concept name and an access token this function returns the dictionary model for the given raw concept.
	This method is called as a part of processing on user input during registration.
	The top-scoring result of a call to annotateText *should*, in ordinary cases, correspond with the article-name of the concept.
	This result is then run through event_insight_lib.fetchRelatedConcepts().
	"""
	# Fetch the precise name of the node (article title) associated with the institution.
	_concept_node = event_insight_lib.annotateText(institution, token)
	# If the correction call is successful, keep going.
	if 'annotations' in _concept_node.keys() and len(_concept_node['annotations']) != 0:
		_concept_node_title = _concept_node['annotations'][0]['concept']['label']
		_related_concepts = event_insight_lib.fetchRelatedConcepts(_concept_node_title, token)
		return parseRawConceptCall(_related_concepts, cutoff)
	# Otherwise, if the call was not successful, return a None flag.
	else:
		return None

def fetchConceptsForEvent(event_string, token, cutoff=0.2):
	"""
	Returns the result of a Watson query against an event string.
	Decorator for event_insight_lib.annotateText() that adds a cutoff parameter.
	TODO: Test!
	"""
	return parseRawEventCall(event_insight_lib.annotateText(event_string, token), cutoff)

def parseRawConceptCall(raw_output, cutoff=0.5):
	"""
	Parses the raw results of a call to the `label_search` IBM Watson API, implementing a cutoff in the process.
	Used to parse the results for  the `fetchConceptsForUserConcept()` front-facing method.
	Returns a dict that can be assigned to an ObjectModel.
	Minor semantic differences from `parseRawEventCall()`, below.
	"""
	dat = dict()
	# If there is nothing to parse, don't parse it.
	if 'concepts' not in raw_output.keys():
		return dat
	else:
		for concept in raw_output['concepts']:
			if concept['score'] >= cutoff:
				dat[concept['concept']['label']] = concept['score']
	return dat

def parseRawEventCall(raw_output, cutoff=0.5):
	"""
	Parses the raw results of a call to the `label_search` IBM Watson API, implementing a cutoff in the process.
	Used to parse the results for  the `fetchConceptsForEvent()` front-facing method.
	Returns a dict that can be assigned to an ObjectModel.
	Minor semantic differences from `parseRawConceptCall()`, above.
	"""
	dat = dict()
	# If there is nothing to parse, don't parse it.
	if 'annotations' not in raw_output.keys():
		return dat
	else:
		for concept in raw_output['annotations']:
			if concept['score'] >= cutoff:
				dat[concept['concept']['label']] = concept['score']
	return dat

###################
# END WATSON/CORE #
###################