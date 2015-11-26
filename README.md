##About
The Cultural Insight tool is a web-based Bluemix-hosted cultural engagement tool. Users of the web portal are able to sign up for a weekly email service which sends them a shortlist of events happening in New York City that, based on a model of that user's interests, they would be interested in attending. The recommendation engine is implemented in Python using the Concept Insight IBM Watson tool; the webservice is implemented in Python Flask. The idea behind this application is that it will funnel the vast amount of information thrown at those that live in the city down to a core of causes that they care about, increasing their engagement by surfacing events that they are actually interested in attending.

##Structure of the application
**Procfile** - This command is run whenever the application is restarted on Bluemix. In our case it runs `app.py`, which defines this system's webservice.

**requirements.txt** - Contains the external python packages that are required by the application. These will be downloaded from the [python package index](https://pypi.python.org/pypi/) and installed via the python package installer (pip) during the buildpack's compile stage when you execute the cf push command. To ensure compatability, use a `virtualenv` configured for Python 3.4.3 and deploy these same packages with `pip -r requirements.txt` on your development machine as well.

**runtime.txt** - Controls which python runtime to use. In our case the entire contents of the file is `python-3.4.3`. 

**README.md** - This readme.

**app.py** - The python web app, implemented in Python [Flask](http://flask.pocoo.org/). The routes are defined in the application using the @app.route() calls. The application deployed to Bluemix needs to listen to the port defined by the VCAP_APP_PORT environment variable as seen here:
```python
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
```

This is the port given to your application so that http requests can be routed to it. If the property is not defined then it falls back to port 5000 allowing you to run this sample appliction locally.

The `/templates` and `/static` folders contain the resources (HTML, CSS, SVG, etc.) used by the web application.

**forms.py** - Simple Flask file storing handling for the forms used by the `app.py` front-end.

**event_insight_lib.py** - The IBM Watson API bindings that I have written for the purposes of this tool.

**event_insight.py** - Test module for `event_insight_lib.py` and for `backend.py`.

**backend.py** - The core of the application, this library contains all of the methods which are called by the various front-ends: the web application (`app.py`), the curation tool (`curator.py`), and the email script (`emailer.py`).

**curator.py** - This administrative script is used in the command line for defining the events that make up this application's event library. It is designed for use by a master "content curator".

**emailer.py** - This script executes the weekly emailings. It should be scheduled as a chron job.

**accounts.json** - Stores the account information. Interacts with the web-app.

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

Define methods for `events.json`. Write the curation tool, `curator.py`.

Write `emailer.py`.

Write concept interaction into the emails.

Finish up the web-application: concept display and account credential changes.