##About
The Cultural Insight tool is a web-based Bluemix-hosted cultural engagement tool. Users of the web portal are able to find events happening in New York City which, based on a model of that user's interests, they would be interested in attending. The recommendation engine is implemented in Python using the Concept Insight IBM Watson tool; the webservice is implemented in Python Flask. The idea behind this application is that it will funnel the vast amount of information thrown at those that live in the city down to a core of causes that they care about, increasing their engagement by surfacing events that they are actually interested in attending.

This example application is a relatively sophisticated demonstratory implementation of a Watson-based recommendation engine, implemented as an example of the kinds of applications that are possible using the service. It can be split into two parts:

* A core collection of methods and classes which together compose a recommendation engine based on the IBM Watson "Concept Insights" API service.

* An example webservice using this technology, presented online on [Bluemix](http://cultural-insight.mybluemix.net/).

##Structure of the application
**Procfile** - This command is run whenever the application is restarted on Bluemix. In our case it runs `app.py`, which defines this system's webservice.

**requirements.txt** - Contains the external python packages that are required by the application. These will be downloaded from the [python package index](https://pypi.python.org/pypi/) and installed via the python package installer (pip) during the buildpack's compile stage when you execute the cf push command. To ensure compatability, use a `virtualenv` configured for Python 3.4.3 and deploy these same packages with `pip -r requirements.txt` on your development machine as well.

**runtime.txt** - Controls which python runtime to use. In our case the entire contents of the file is `python-3.4.3`. 

**README.md** - This readme.

**app.py** - The Python web app, implemented in Python [Flask](http://flask.pocoo.org/). The routes are defined in the application using the @app.route() calls. The application deployed to Bluemix needs to listen to the port defined by the VCAP_APP_PORT environment variable as seen here:
```python
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
```

This is the port given to your application so that http requests can be routed to it. If the property is not defined then it falls back to port 5000 allowing you to run this sample appliction locally.

The `/templates` and `/static` folders contain the resources (HTML, CSS, SVG, etc.) used by the web application.

**forms.py** - Simple `Form` classfile file storing the `flask-wtf` forms used by the `app.py` front-end.

**event_insight_lib.py** - The IBM Watson API bindings that I have written for the purposes of this tool. This will hopefully one day be deprecated in favor of the [Watson Developer Cloud Python SDK](https://github.com/watson-developer-cloud/python-sdk).

**backend.py** - This library contains a methods which are called by the various front-ends. In the process of being distributed out to other files.

**curator.py** - This administrative script is used in the command line for defining the events that make up this application's event library. It is designed for use by a master "content curator". Note: needs rewriting.

**emailer.py** - This script executes the weekly emailings. It should be scheduled as a chron job. Not currently in active development (this is a stretch goal).

**accounts.json** - Stores the account information. Interacts with the web-app. Of the form:

```
{
    "accounts": [
        {
            "email": "Email"
            "password": "Password",
            "model": {
                "maturity": 1,
                "concepts": {
                    "Test": 0.5
                },
            "exceptions": [
                "Jackson Pollack Exhibit",
                "etc."
            ]
            }
        }
    ]
}
```


**events.json** - Stores the events information. Interacts with the emailer and curation scripts. Of the form:

```
{
    "events": [
        {
            "name": "Name",
            "description": "Long description...",
		    "start-time": [
    		    2015,
 		       	11,
 		       	26,
 		       	0,
 		       	0,
 		       	54,
 		       	3,
 		       	330,
		       	0
		        ],
		    "end-time": [
    		    2015,
 		       	11,
 		       	26,
 		       	0,
 		       	0,
 		       	54,
 		       	3,
 		       	330,
		       	0
		        ],
            "model": {
                "concepts": {
                    "United States Department of the Interior": 0.663,
                    "Bronze": 0.713,
                    "Museum of Modern Art": 0.513,
                    "..." : 0.000,
                }
            }
        }
    ]
}
```

**token.json** - Stores the token used for accessing IBM Watson services. Each token lives for only an hour. Of the form:

```
{
    "time": [
        2015,
        11,
        26,
        0,
        0,
        54,
        3,
        330,
        0
    ],
    "token": "long string..."
}

```

**concent_insight_credential.json** - Stores the permanent access key for the IBM Watson Concept Insight service used by this application. Included in `.gitignore` and not posted to the online repository, for obvious reasons. Of the form:

```
{
  "credentials": {
    "url": "https://gateway.watsonplatform.net/concept-insights/api",
    "username": "..."
    "password": "..."
  }
}
```

**sendgrid_key.json** - Stores the SendGrid Bluemix service key used by the emailer application. Included in `.gitignore` and thus excluded from the online repository, for obvious reasons. Of the form:

```
{
  "api_key" : "...key..."
}
```

##To do

Finish OOP code rebase.

Continue to populate an example list of events, using `curator.py`.

Stetch goal: Write `cleanup.py`.

Stretch goal: Write `emailer.py`.