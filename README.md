#Py-Events

##Structure of application
**Procfile** - Contains the command to run when you application starts on Bluemix. It is represented in the form `web: <command>` where `<command>` in this sample case is to run the `py` command and passing in the the `welcome.py` script.

**requirements.txt** - Contains the external python packages that are required by the application. These will be downloaded from the [python package index](https://pypi.python.org/pypi/) and installed via the python package installer (pip) during the buildpack's compile stage when you execute the cf push command. In this sample case we wish to download the [Flask package](https://pypi.python.org/pypi/Flask) at version 0.10.1

**runtime.txt** - Controls which python runtime to use. In this case we want to use 2.7.9. 

**README.md** - this readme.

**app.py** - the python application script. This is implemented as a simple [Flask](http://flask.pocoo.org/) application. The routes are defined in the application using the @app.route() calls. This application has a / route and a /myapp route defined. The application deployed to Bluemix needs to listen to the port defined by the VCAP_APP_PORT environment variable as seen here:
```python
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
```

This is the port given to your application so that http requests can be routed to it. If the property is not defined then it falls back to port 5000 allowing you to run this sample appliction locally.

##Notes
Urgently needs investigating: https://developer.ibm.com/answers/questions/233701/why-is-there-such-a-large-difference-between-simul.html
