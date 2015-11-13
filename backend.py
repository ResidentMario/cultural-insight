'''backend.py
    This library implements the data interface methods used by the app.py webservice. It is meant to serve as a library for use thereof.
    This means that only methods related to using the website go here: the email service is defined seperately, in email_service.py.
    Unit testing for this library is present at test.py.
    TODO: Figure out that organization.'''

import json
import os
import random

############
# SENDGRID #
############
# SendGrid is IBM Watson's technology solution partner for email services.
# The methods that follow are based on the SendGrid Pythonic API (https://github.com/sendgrid/sendgrid-python).

import sendgrid

# SendGrid secret key.
api_key = None

'''Loads the SendGrid secret key from its JSON storage file. Called by the `sendEmail()` meta-method.'''
def fetchSendGridKey(filename='sendgrid_key.json'):
	return json.load(open(filename))['api_key']

'''Generic email template, implemented using the SendGrid emailer service. Extended by application-specific methods.'''
def sendEmail(_to, _from, subject, content):
	# Fetch the SendGrid key from the hidden JSON keyfile, if it has not been defined already.
	if api_key == None:
		api_key = fetchSendGridKey()
	sg = sendgrid.SendGridClient(api_key)
	message = sendgrid.Mail()
	message.add_to(_to)
	message.set_from(_from)
	message.set_subject(subject)
	message.set_html(content)
	chk = sg.send(message)
	# The SendGrid send method returns a tuple (http_status_code, message) that I return here for debugging purposes.
	return chk

################
# END SENDGRID #
################

#############
# INTERFACE #
#############
# This section contains all of the backend methods servicing the user interface layer of the webservice.

'''Checks if an email is already in use. Returns True if it is, False if not.'''
def emailAlreadyInUse(new_email, filename='accounts.json'):
	# Open the accounts file.
	if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
		list_of_users = json.load(open(filename))['accounts']
	# Check to see if the selected email appears in the list.
	for existing_user in list_of_users:
		if existing_user['email'] == new_email:
			return True
	return False

'''Adds an email to the accounts file.
	The interests field is a dummy variable, for now. It is expected to be a list of three to ten elements.
	TODO: Thread Concept Insights through the inputted interests (see `conceptualize`), splice together an early model, and log that.'''
def addNewUser(new_user_email, new_user_password, new_user_institutions_list, filename='accounts.json'):
	# Open the JSON file.
	if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
		user_data = json.load(open(filename))
	# Append the new user.
	user_data['accounts'].append({'email': new_user_email, 'password': new_user_password, 'concepts': conceptualize(new_user_institutions_list)})
	# Re-encode and save the modified file.
	with open(filename, 'w') as outfile:
		json.dump(user_data, outfile)

'''Authenticates a user's email-password combination.'''
def authenticateUser(email, password, filename='accounts.json'):
	if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
		list_of_users = json.load(open(filename))['accounts']
	# Check to see if the selected email appears in the list.
	for existing_user in list_of_users:
		if existing_user['email'] == email and existing_user['password'] == password:
			return True
	return False

'''Deletes an account. May be requested by the user via the dashboard, or via an administrative script.
	TODO: admintools?
	TODO: Implement.'''
def deleteAccount():
	pass

'''Changes the email associated with an account. Must be requested by the user via the dashboard.
	TODO: Implement. The method below does not quite work. Needs a while loop.'''
def changeEmail(current_email, new_email, filename='accounts.json'):
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

'''Changes the password associated with an account. Must be requested by the user via the dashboard.
	TODO: Implement.'''
def changePassword(current_email, new_password, filename='accounts.json'):
	pass

'''Imports the secret string used by some of the Flask plug-ins for security purposes.
	The secret string is be a simple randomly generated numerical, defined at runtime.'''
def initializeSecretString():
	return random.random()

#################
# END INTERFACE #
#################

###############
# WATSON/CORE #
###############
# This section contains the systemic core of the application---its interface with the IBM Watson Concept Insights service.

'''A statistically analytical method which atomizes a given list of objects and turns them into a ranked list of concepts.
	Concepts are arranged {'Concept': <NAME>, 'Score': <SCORE> }, where SCORE is the mean confidence returned by Concept Insight when
	called along the series.
	Pass-method for now, still to be implemented.
	Inputs a list of concepts, outputs a dictionary of concepts (as above).
	Called by addNewUser(). Implements addObjectToConceptModel().
	TODO: Implement!'''
def conceptualize(list_of_things):
	return list_of_things

'''A statistically analytical method which atomizes a given concept and fuses it into an existing (possibly empty) ranked list of concepts.
	This method is an internal submethod of conceptualize, which basically just calls this method multiple times (or once).
	TODO: Implement!'''
def addObjectToConceptModel(object, concept_model):
	pass

'''Compares two concept models and returns a standardized measure of overlap. Open question: two-iter, or one-iter?
	Two-iter would be more accurate, especially with low information, but more costly, and harder to implement. Might be necessary?
	Input is a pair of object models.
	Output is a standardized 0-to-1 real describing correlation.
	This method is used by the email script.
	TODO: Implement!'''
def compareConceptModels():
	pass

'''Returns a user email iterator. Used by the email script.
	Should I be using an iterator? It's not neccessary, probably, but I need to use a little bit of flair, for practice. :)
	NOTE: Untested.'''
def iterEmails(filename='accounts.json'):
	if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
		user_data = json.load(open(filename))
	yield user_data['email']

'''Helper function for saving a file. Not currently used.'''
def saveFile(content, filename):
	f = open(filename, 'w')
	f.write(json.dumps(content, indent=4))
	f.close()

###################
# END WATSON/CORE #
###################