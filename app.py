import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__)

# Returns a static index page with a simple form to fill out.
# TODO: Dynamic forms. Investigate flask-wtf.
@app.route('/')
def indexPage():
    return render_template('index.html')

# The application itself. Just a proof of concept for the moment, to show that it can be done.
@app.route('/query', methods=['GET', 'POST'])
def query():
	a = b = c = ''
	if request.method == 'POST':
		a = request.form['first_event']
		b = request.form['second_event']
		c = request.form['third_event']
		# Pass through a template rendering.
		return a + b + c
	# If the user inputs `/query` directly in their web browser, just redirect them back to the front page.
	else:
		return redirect("..", code=302)


###################################
# RUNTIME CODE
# `VCAP_APP_PORT` is the port that Bluemix servers are configured to pass and run on.
# When run locally this code will not be able to define this variable and fall back on the default port, 5000.
# This allows this application to handle being run both locally and server-side with the same runtime method.
###################################
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))