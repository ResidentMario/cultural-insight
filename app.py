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

# My own libraries.
import forms
import backend

app = Flask(__name__)

# SPLASH: The homepage is a static page consisting of a short description of what this project is all about and two bottons,
# one pointing to logins and one point to signups.
@app.route('/')
def splash():
    return render_template('splash.html')

# START: On this page users enter the information which the application will use to route them their event information.
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
				# This is where the bulk of the effort in this program is. It will call on methods in event_insight_lib.py.
				# TODO: Implement waiting loop, since the previous step is probably going to take a few seconds.
				# "But Aleksey, you can do it asynchronously! Oh, sure, just give me...a week?" "Yeah, never mind."
				backend.addNewUser(request.form['email'], request.form['password'], [request.form['i1'], request.form['i2'],
				 request.form['i3'], request.form['i4'], request.form['i5'], request.form['i6'], request.form['i7'], request.form['i8'],
				 request.form['i9'], request.form['i10']])
				return render_template('registered.html')
		else:
			return render_template('start.html', form=form, error='Error: You must input all of the required fields.')

@app.route('/login.html')
def login():
	return render_template('login.html')

###################################
# RUNTIME CODE
# `VCAP_APP_PORT` is the port that Bluemix servers are configured to pass and run on.
# When run locally this code will not be able to define this variable and fall back on the default port, 5000.
# This allows this application to handle being run both locally and server-side with the same runtime method.
###################################
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))