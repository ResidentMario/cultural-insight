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

##################
# SENDGRID/EMAIL #
##################
# SendGrid is IBM's technology solution partner for email services.
# The methods that follow are based on the SendGrid Pythonic API (https://github.com/sendgrid/sendgrid-python).

import sendgrid

# SendGrid secret key.
api_key = None

def fetchSendGridKey(filename='sendgrid_key.json'):
	"""Loads the SendGrid secret key from its JSON storage file. Called by `generateEmail()`, and by `sendEmail()` from there."""
	return json.load(open(filename))['api_key']

def generateEmail(subject, content):
	"""
	Generates a sendgrid.Mail() object containing the given subject and content.
	Returns the object.
	"""
	message = sendgrid.Mail()
	message.set_subject(subject)
	message.set_html(content)
	# Note: to get only the subject use .subject, to get only the body use ??? .content is a dict, need to do a bit of plumbing.
	# The SendGrid API doesn't have any getter methods?
	return message

def sendEmail(_to, _from, subject, content):
	"""Generic email template, implemented using the SendGrid emailer service. Extended by application-specific methods."""
	# Fetch the SendGrid key from the hidden JSON keyfile, if it has not been defined already.
	if api_key == None:
		api_key = fetchSendGridKey()
	sg = sendgrid.SendGridClient(api_key)
	message = generateEmail(subject, content)
	message.add_to(_to)
	message.set_from(_from)
	chk = sg.send(message)
	# The SendGrid send method returns a tuple (http_status_code, message) that I return here for debugging purposes.
	return chk

def iterEmails(filename='accounts.json'):
	"""
	Returns a user email iterator. Used by the email script.
	Should I be using an iterator? It's not neccessary, probably, but I need to use a little bit of flair, for practice. :)
	NOTE: Untested.
	"""
	if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
		user_data = json.load(open(filename))
	yield user_data['email']

######################
# END SENDGRID/EMAIL #
######################

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

def addNewUser(new_user_email, new_user_password, new_user_institutions_list, filename='accounts.json'):
	"""
	Adds an email to the accounts file.
	The interests field is a dummy variable, for now. It is expected to be a list of three to ten elements.
	TODO: Thread Concept Insights through the inputted interests (see `conceptualize()`), splice together an early model, and log that.
	"""
	# Open the JSON file.
	if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
		user_data = json.load(open(filename))
	# Initialize the concept model.
	concept_model = {'maturity': 1, 'concepts': conceptualize(new_user_institutions_list)}
	# Append the new user.
	user_data['accounts'].append({'email': new_user_email, 'password': new_user_password, 'model': concept_model})
	# Re-encode and save the modified file.
	saveFile(user_data, filename)
	# with open(filename, 'w') as outfile:
	# 	json.dump(user_data, outfile)

def authenticateUser(email, password, filename='accounts.json'):
	"""Authenticates a user's email-password combination."""
	if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
		list_of_users = json.load(open(filename))['accounts']
	# Check to see if the selected email appears in the list.
	for existing_user in list_of_users:
		if existing_user['email'] == email and existing_user['password'] == password:
			return True
	return False

def deleteAccount():
	"""
	Deletes an account. May be requested by the user via the dashboard, or via an administrative script.
	Or, you know, by hand.
	TODO: admintools?
	TODO: Implement.
	"""
	pass

def changeEmail(current_email, new_email, filename='accounts.json'):
	"""
	Changes the email associated with an account. Must be requested by the user via the dashboard.
	TODO: Implement. The method below does not quite work. Needs a while loop.
	"""
	#if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
	#	list_of_users = json.load(open(filename))['accounts']
	## Check to see if the selected email appears in the list.
	#for existing_user in list_of_users:
	#	if existing_user['email'] == current_email:
	#		existing_user['email'] = new_email
	#		with open(filename, 'w') as outfile:
	#			json.dump(list_of_users, outfile)
	#		break
	pass			

def changePassword(current_email, new_password, filename='accounts.json'):
	"""
	Changes the password associated with an account. Must be requested by the user via the dashboard.
	TODO: Implement.
	"""
	pass

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

class ConceptModel:
	"""The ConceptModel object handles all of the concept model abstraction."""
	maturity = 1
	model = dict()
	email = ''

	def __init__(self, _model=dict(), _email=''):
		self.loadModel(_email)
		self.email = _email

	def loadModel(self, email, filename='accounts.json'):
		"""Given the email of a registered user, loads a single user's model out of the accounts list."""
		list_of_users = json.load(open(filename))['accounts']
		for user in list_of_users:
			if user['email'] == email:
				self.model = user['model']['concepts']
				break

	def saveModel(self, filename='accounts.json'):
		"""Given the concept model and email of a registered user, saves their model to the accounts list."""
		data = json.load(open(filename))
		for i in range(0, len(data['accounts'])):
			if data['accounts'][i]['email'] == self.email:
				data['accounts'][i]['model']['concepts'] = self.model
				break
		# Re-encode and save the modified file.
		with open(filename, 'w') as outfile:
			json.dump(data, outfile)

def getToken(tokenfile='token.json'):
	"""
	This is the primary-use access method meant to be used throughout the application.
	Path-wrapper for the getToken() method in event_insight_lib.py.
	"""
	return event_insight_lib.getToken(tokenfile)

def addNewUser(user_email, user_password, user_institutions_list, token, filename='accounts.json'):
	"""
	Font-facing method, which called from app.py, handles all of the work of registering a user.
	Takes as a parameter the name of the user, their password, and a list consisting of all of the institutions to be assigned.
	NOTE: This is the method that is called by the webapp as the final step of the registration process.
	"""
	user = ConceptModel()
	user.model = conceptualize(user_institutions_list, token)
	user.email = user_email
	data = json.load(open(filename))
	data['accounts'].append(
        {
            "password": user_password,
            "model": {
                "concepts": user.model,
                "maturity": 1
            },
            "email": user_email
        })
	# Re-encode and save the modified file.
	with open(filename, 'w') as outfile:
		json.dump(data, outfile, indent=4)
	return user.model

def conceptualize(list_of_things, token, cutoff=0.5):
	"""
	A method which atomizes a given list of institutions and turns them into a ranked list of concepts.
	Called by the `addNewUser()` front-end method.
	Implements `fetchConceptsForInstitution()` and `addObjectToConceptModel()`.
	Returns a ConceptModel.model sub-object dictionary.
	"""
	dat = ConceptModel()
	for thing in list_of_things:
		new = ConceptModel()
		new.model = fetchConceptsForInstitution(thing, token)
		# If a new model fails definition it will return a None flag.
		# This signals to this method that it shouldn't bother trying to merge the one into the other, since there's nothing to merge.
		if new.model != dict() and new.model != None:
			dat = addObjectToConceptModel(dat, new)
	return dat.model

def addObjectToConceptModel(base_concept_model, merger_concept_model):
	"""
	This method merges two ConceptModel objects into one, using a running average.
	One concept model is considered the base, one is considered the merger.
	This is because, generally speaking, you will want to be adding fresh data into an already well-defined model.
	TODO: Tweak math a little bit to account for the number of objects being merged in.
	Returns the merged ConceptModel object.
	"""
	new_concept_model = ConceptModel()
	new_list = []
	# Increment the maturity of the model.
	new_concept_model.maturity = base_concept_model.maturity + merger_concept_model.maturity
	# Match up and average the concepts.
	bK = sorted(base_concept_model.model.keys())
	mK = sorted(merger_concept_model.model.keys())
	for pair in itertools.zip_longest(bK, mK, fillvalue=None):
		if pair[0] == pair[1]:
			new_concept_model += { pair[0]: round((bK[int(pair[0])]*base_concept_model.maturity + mK[int(pair[0])]*merger_concept_model.maturity)/new_concept_model.maturity,3) }
		else:
			if pair[0] != None:
				new_concept_model.model.update({ pair[0]: round(base_concept_model.model[pair[0]]*base_concept_model.maturity/new_concept_model.maturity,3) })
			if pair[1] != None:
				new_concept_model.model.update({ pair[1]: round(merger_concept_model.model[pair[1]]*merger_concept_model.maturity/new_concept_model.maturity,3) })
	return new_concept_model

def compareConceptModels(first_concept_model, second_concept_model):
	"""
	Compares two concept models and returns a measure of average overlap (a mock correlation).
	Input is a pair of object models.
	Open question: two-iter, or one-iter?
	Two-iter would be more accurate, especially with low information, but more costly, and harder to implement. Might be necessary?
	Another open question is whether or not a more sophisticated model could or should be used.
	Output is a standardized 0-to-1 three-decimal number describing correlation.
	This method is used by the email script.
	"""
	overlap = 0
	num = 0
	for pair in zip(sorted(first_concept_model.model.keys()), sorted(second_concept_model.model.keys())):
		if pair[0] == pair[1]:
			overlap += first_concept_model.model[pair[0]] + second_concept_model.model[pair[1]]
			num += 1
	if num == 0:
		return 0.0
	else:
		return round((overlap/num)/min(len(first_concept_model.model),len(second_concept_model.model)),3)

def fetchConceptsForInstitution(institution, token, cutoff=0.5):
	"""
	Given the name of an institution and an access token this function returns the dictionary model for the given cultural institution.
	This method is called as a part of processing on user input during registration.
	The top-scoring result of a call to annotateText *should*, in ordinary cases, correspond with the article-name of the institution.
	CRITICAL: This is simply *not* very robust! For now we have to ask that users try to hew as closely as possible to the official names
	of the institutions they are entering. Otherwise their results are discarded.
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
	# return event_insight_lib.annotateText(event_string, token)
	# return event_insight_lib.annotateText(event_string, token)['annotations'].keys()
	# if 'annotations' in _concept_node.keys() and len(_concept_node['annotations']) != 0:
	return parseRawEventCall(event_insight_lib.annotateText(event_string, token), cutoff)

def parseRawConceptCall(raw_output, cutoff=0.5):
	"""
	Parses the raw results of a call to the `label_search` IBM Watson API, implementing a cutoff in the process.
	Used to parse the results for  the `fetchConceptsForInstitution()` front-facing method.
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

def saveFile(content, filename):
	"""Helper function for saving a file."""
	f = open(filename, 'w')
	f.write(json.dumps(content, indent=4))
	f.close()

###################
# END WATSON/CORE #
###################