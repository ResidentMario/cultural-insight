'''app.py
    This file implements this application's webservice: specifically, only those aspects of the program related to pagation and interface.
    Back-end methods, primarily those related to the data interface, are defined in backend.py. ???
    The email service is defined seperately, in email_service.py. ???
    Testing methods go into test.py. ???
    TODO: Figure out that organization.
    TODO: Investigate flask-email and flask-login. Will need them in this architecture.'''

# Redistributables.
import os
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
# TODO: Move to backend.py?

import flask.ext.login as flask_login

# Initialize the login manager.
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

'''The default User class implemented by Flask-Login is fine for our purposes.'''
class User(flask_login.UserMixin):
    pass

'''The user loader implemented by Flask-Login loads a user via email.'''
@login_manager.user_loader
def user_loader(email):
	if not backend.emailAlreadyInUse(email):
		return
	else:
		user = User()
		user.id = email
		return user

'''The user loader implemented by Flask-Login loads a user via request form.'''
@login_manager.request_loader
def request_loader(request):
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

'''SPLASH: The homepage is a static page consisting of a short description of what this project is all about and two bottons.
One button points to logins and one point to signups.'''
@app.route('/')
def splash():
    return render_template('splash.html')

'''START: On this page users enter the information which the application will use to route them their event information.'''
@app.route('/start.html', methods=['GET', 'POST'])
def start():
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
				# Now we have the data, contained in request.form['password'], email, i1, ..., i10. We have to process it somehow.
				backend.addNewUser(request.form['email'], request.form['password'], [request.form['i1'], request.form['i2'],
				 request.form['i3'], request.form['i4'], request.form['i5'], request.form['i6'], request.form['i7'], request.form['i8'],
				 request.form['i9'], request.form['i10']])
				flash('Your account was successfully registered.')
				return render_template('registered.html')
		else:
			return render_template('start.html', form=form, error='Error: You must input all of the required fields.')

'''LOGIN: This is the page on which users log into the application.'''
@app.route('/login.html', methods=['GET', 'POST'])
def login():
	form = forms.LoginForm(csrf_enabled=False)
	if request.method == 'GET':
		return render_template('login.html', form=form)
	else:
		if backend.authenticateUser(request.form['email'], request.form['password']):
			user = User()
			email = request.form['email']
			user.id = email
			flask_login.login_user(user)
			flash('You were successfully logged in.')
			return redirect('/')
		else:
			return render_template('login.html', form=form, error='Error: Incorrect username or password.')

'''LOGOUT: A simple confirmation that redirects to the homepage.'''
@app.route('/logout.html')
def logout():
    flask_login.logout_user()
    flash('You were successfully logged out.')
    return redirect('/')

'''DASHBOARD: This is where all of the user account controls live.'''
@app.route('/dashboard.html', methods=['GET', 'POST'])
def dashboard():
	form = forms.DashboardForm(csrf_enabled=False)
	if request.method == 'GET':
		return render_template('dashboard.html', form=form)
	if request.method == 'POST':
		if request.form['email']:
			backend.changeEmail(flask_login.current_user.get_id(), request.form['email'])
		if request.form['password']:
			backend.changePassword(flask_login.current_user.get_id(), request.form['password'])
		flash('Your changes have been applied. You may now log back in again.')
		return render_template('dashboard.html', form=form)

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
	# app.run(host='0.0.0.0', port=int(port), debug=True)
	app.run(host='0.0.0.0', port=int(port))