Note: the original structure of this application is from IBM's [Flask Bluemix sample](https://github.com/IBM-Bluemix/bluemix-python-flask-sample).

##Structure of the application
**Procfile** - Contains the command to run when you application starts on Bluemix. It is represented in the form `web: <command>` where `<command>` in this sample case is to run the `py` command and passing in the the `app.py` script.

**requirements.txt** - Contains the external python packages that are required by the application. These will be downloaded from the [python package index](https://pypi.python.org/pypi/) and installed via the python package installer (pip) during the buildpack's compile stage when you execute the cf push command.

**runtime.txt** - Controls which python runtime to use. In this case we want to use 3.4.3. 

**README.md** - this readme.

**app.py** - the python application script. This is implemented as a simple [Flask](http://flask.pocoo.org/) application. The routes are defined in the application using the @app.route() calls. This application has a / route and a /myapp route defined. The application deployed to Bluemix needs to listen to the port defined by the VCAP_APP_PORT environment variable as seen here:
```python
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
```

This is the port given to your application so that http requests can be routed to it. If the property is not defined then it falls back to port 5000 allowing you to run this sample appliction locally.

##Development plan.

Log-ins, via flask-login.

Emails sending and content skeleton, via flask-email.

Commanded script-based methods for adding events to the master list.

Define a 100 (?)-event starter dataset manually.

Flushing out IBM Watson methods.

Email job scheduling.