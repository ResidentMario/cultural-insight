"""
app.py
This Flask file implements this application's webservice.
"""

# Redistributables.
import os
import json
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

# My own libraries.
import forms
import backend

# Declarative.
app = Flask(__name__)

# The secret key is used by both flask-login and flask-flash
app.secret_key = str(backend.initializeSecretString())

########
# CSRF #
########
# TODO: CSRF is code injection attack protection. I need to work out how to implement this for the production verison.
# For now it's just disabled on all forms: see the csrf_enabled=false arguments throughout.
# from flask_wtf.csrf import CsrfProtect
# CsrfProtect(app)

################
# FLASK-LOGIN  #
# ##############
# This subsection controls how users log in and out of the webservice.
# It uses the Flask-Login package.
# See also `user.py`, which contains the methods associated with the application's individual users;
# and `conceptmodel.py`, which contains the methods associated with each user's individual conceptualization.

import flask.ext.login as flask_login
from user import User
from conceptmodel import ConceptModel

# Initialize the login manager.
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(email):
	"""The user loader implemented by Flask-Login loads a user via email."""
	if not backend.emailAlreadyInUse(email):
		return
	else:
		user = User().loadUser(email)
		user.id = email
		return user

@login_manager.request_loader
def request_loader(request):
	"""The user loader implemented by Flask-Login loads a user via request form."""
	email = request.form.get('email')
	password = request.form.get('password')
	if not backend.authenticateUser(email, password):
		return
	else:
		user = User()
		user.id = email
		return user

###################
# END FLASK-LOGIN #
###################

#########
# PATHS #
#########

@app.route('/')
def splash():
	"""
	SPLASH: The homepage is a static page consisting of a short description of what this project is all about and two bottons.
	One button points to logins and one point to signups.
	"""
	return render_template('splash.html')

@app.route('/start.html', methods=['GET', 'POST'])
def start():
	"""START: On this page users enter the information which the application will use to route them their event information."""
	form = forms.StartForm(csrf_enabled=False)
	if request.method == 'GET':
		return render_template('start.html', form=form)
	else:
		if request.form['password'] and request.form['email'] and request.form['i1'] and request.form['i2'] and request.form['i3']:
			if backend.emailAlreadyInUse(request.form['email']):
				return render_template('start.html', form=form, error='Error: The email you have chosen is already in use.')
			elif 'baruch' not in request.form['email']:
				return render_template('start.html', form=form, error='Error: Please input a Baruch email, only, please! Other email addresses are not supported yet.')
				# TODO: To support other email addresses we can use the flask-wtf validate email subroutine.
			else:
				user = User(email=request.form['email'], password=request.form['password'])
				concepts = [concept for concept in [request.form['i1'], request.form['i2'], request.form['i3'], request.form['i4'], request.form['i5']] if concept != '']
				for concept in concepts:
					user.addUserInputToConceptModel(concept)
				user.saveUser()
				flask_login.login_user(user)
				flash('Your account was successfully registered.')
				return render_template('registered.html')
		else:
			return render_template('start.html', form=form, error='Error: You must input all of the required fields.')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
	"""LOGIN: This is the page on which users log into the application."""
	form = forms.LoginForm(csrf_enabled=False)
	if request.method == 'GET':
		return render_template('login.html', form=form)
	else:
		if backend.authenticateUser(request.form['email'], request.form['password']):
			user = User().loadUser(request.form['email'])
			flask_login.login_user(user)
			flash('You were successfully logged in.')
			return redirect('/')
		else:
			return render_template('login.html', form=form, error='Error: Incorrect username or password.')

@app.route('/logout.html')
def logout():
	"""LOGOUT: A simple confirmation that redirects to the homepage."""
	flask_login.logout_user()
	flash('You were successfully logged out.')
	return redirect('/')

@app.route('/suggestion.html' , methods=['GET', 'POST'])
def suggest():
	"""SUGGESTIONS: This is where the user views and interacts with suggested events and exhibitions."""
	form = forms.SuggestionForm(csrf_enabled=False)
	event = flask_login.current_user.getBestEvent()
	# return event.name
	if request.method == 'GET':
		return render_template('suggestion.html', event=event)
	elif request.method == 'POST' and form.validate_on_submit():
		# User requests we show more events like this one.
		# In this case we merge that event's concept model into the user's model and we add the given event to our list of exceptions.
		if 'More' in request.form:
			flask_login.current_user.getConceptModel().iterateModel(event.model)
			flask_login.current_user.exceptions.append(event.name)
			flask_login.current_user.saveUser()
			flash('Your preferences have been updated!')
			return render_template('suggestion.html', event=event)
		# User requests we show fewer events like this one.
		# In this case we simply add the event to our list of exceptions for this user.
		elif 'Less' in request.form:
			flask_login.current_user.exceptions.append(event.name)
			flask_login.current_user.saveUser()
			flash('Your preferences have been updated!')
			return render_template('suggestion.html', event=event)

@app.route('/dashboard.html', methods=['GET', 'POST'])
def dashboard():
	"""DASHBOARD: This is where all of the user account controls live."""
	form = forms.DashboardForm(csrf_enabled=False)
	if request.method == 'GET':
		# return str(list(flask_login.current_user.getConceptModel().model)) + flask_login.current_user.email + flask_login.current_user.get_id() + str(flask_login.current_user.model.maturity)
		return render_template('dashboard.html', form=form, concepts=flask_login.current_user.getConceptModel().model)
	if request.method == 'POST':
		if request.form['email'] or request.form['password']:
			if request.form['email']:
				flask_login.current_user.updateUser(email=request.form['email'])
			if request.form['password']:
				flask_login.current_user.updateUser(password=request.form['password'])
			flask_login.logout_user()
			flash('Your changes have been applied. Please log back in again now.')
			return redirect('/')
		if request.form['i1']:
			# This method is flagged to return False when the operation fails.
			# This occurs when the raw input the user provides is not good enough to resolve to a particular concept.
			# In that case, return an error message indicating this fact.
			flag = flask_login.current_user.addUserInputToConceptModel(request.form['i1'])
			if flag == False:
				return render_template('dashboard.html',
					error='Error: The input you provided could not be resolved.',
					form=form,
					concepts=flask_login.current_user.getConceptModel().mode)
			else:
				flask_login.current_user.saveUser()
				flash('Your changes have been applied.')
				return render_template('dashboard.html', form=form, concepts=flask_login.current_user.getConceptModel().model)

#############
# END PATHS #
#############

###################################
# RUNTIME CODE
# `VCAP_APP_PORT` is the port that Bluemix servers are configured to pass and run on.
# When run locally this code will not be able to define this variable and fall back on the default port, 5000.
# This allows this application to handle being run both locally and server-side with the same runtime method.
###################################
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
	# app.run(host='0.0.0.0', port=int(port))