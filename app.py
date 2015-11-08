import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import forms

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
			return 'Success!'
			# Now we have the data, contained in request.form['password'], email, i1, ..., i10. We have to process it somehow.
			# This is where the bulk of the effort in this program is. It will call on methods in event_insight_lib.py.
			# TODO: Implement!
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
	app.run(host='0.0.0.0', port=int(port), debug=True)