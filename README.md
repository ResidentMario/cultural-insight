##About
The Cultural Insight tool is a web-based Bluemix-hosted cultural engagement tool. Users of the web portal are able to find events happening in New York City which, based on a model of that user's interests, they would be interested in attending. The recommendation engine is implemented in Python using the Concept Insight IBM Watson tool; the webservice is implemented in Python Flask. The idea behind this application is that it will funnel the vast amount of information thrown at those that live in the city down to a core of causes that they care about, increasing their engagement by surfacing events that they are actually interested in attending.

This example application is a relatively sophisticated demonstratory implementation of a Watson-based recommendation engine, implemented as an example of the kinds of applications that are possible using the service. It can be split into two parts:

* A core collection of methods and classes which together compose a recommendation engine based on the IBM Watson "Concept Insights" API service.

* An example webservice using this technology: the [Cultural Insight Application](http://cultural-insight.mybluemix.net/)  (hosted on [Bluemix](https://console.ng.bluemix.net/).


##Using the tool
![Screenshot of the Start Screen](https://raw.githubusercontent.com/ResidentMario/cultural-insight/master/static/images/start-screen.png)

To begin using the Cultural Insight tool head over to the [registration page](http://cultural-insight.mybluemix.net/start.html) and get started with creating your account. You will be asked to provide your email, which will be used as your "ID" throughout the application; your password; and a few of the broad cultural topics that interest you most.

Once you have registered for an account you will be able to log in and begin using the service.

![Screenshot of the Dashboard Screen](https://github.com/ResidentMario/cultural-insight/blob/master/static/images/dashboard-screen.png?raw=true)

The "Account Dashboard" page allows you to modify your account settings. It also allows you to feed the service still further interests, allowing you to manually configure the output that the system returns to you. If there is some category of events that you are interested that the service is not yet able to find, you can input them here and enjoy your expanded search results.

![Screenshot of the Suggestions Screen](https://github.com/ResidentMario/cultural-insight/blob/master/static/images/suggestion-screen.png?raw=true)

The core of the application is the "Suggestions" pane. Here you can see the recommendations on events and going-ons that the system has prepared for your viewing. "Learn More" provides a link to the full event description, while "Show me more like this!" and "Not interested." moves the user on to the next event, incrementing the system's understanding of its user in the meantime.

##Structure of the application
**Procfile** - This command is run whenever the application is restarted on Bluemix. In our case it runs `app.py`, which defines this system's webservice.

**requirements.txt** - Contains the external python packages that are required by the application. These will be downloaded from the [python package index](https://pypi.python.org/pypi/) and installed via the python package installer (pip) during the buildpack's compile stage when you execute the cf push command. To ensure compatability, use a `virtualenv` configured for Python 3.4.3 and deploy these same packages with `pip -r requirements.txt` on your development machine as well.

**runtime.txt** - Controls which python runtime to use. In our case the entire contents of the file is `python-3.4.3`. 

**README.md** - This readme.

**.gitignore** - The usual `.gitignore` file. In particular, `*.json` excludes all of the application's sensitive, locally-stored credentials.

**app.py** - The Python web app, implemented in Python [Flask](http://flask.pocoo.org/). The routes are defined in the application using the @app.route() calls. The application deployed to Bluemix needs to listen to the port defined by the VCAP_APP_PORT environment variable as seen here:

```
python
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
```

This is the port given to your application so that http requests can be routed to it. If the property is not defined then it falls back to port 5000 allowing you to run this sample appliction locally.

**/templates** - The `/templates` and `/static` folders contain the resources (HTML, CSS, SVG, etc.) used by the web application.

**/static** - See above.

**forms.py** - Simple `Form` classfile file storing the `flask-wtf` forms used by the `app.py` front-end.

**event_insight_lib.py** - The IBM Watson API bindings that I have written for the purposes of this tool. This will hopefully one day be deprecated in favor of the [Watson Developer Cloud Python SDK](https://github.com/watson-developer-cloud/python-sdk).

**backend.py** - This library contains a methods which are called by the various front-ends. In the process of being distributed out to other files.

**curator.py** - This administrative script is used in the command line for defining the events that make up this application's event library. It is designed for use by a master "content curator". Written using the `click` library.

**emailer.py** - This script executes the weekly emailings. It should be scheduled as a chron job. Not currently in active development (this is a stretch goal).

**conceptmodel.py** - This classfile defines the `ConceptModel`, the object abstraction for concept insight calls used throughout the application.

**user.py** - This classfile defines the `User`, the object abstraction for the application's current user that's used for tracking credentials and interacting with the User's concept model within `app.py`.

**item.py** - Generic `Item` superclass file that is meant to make the code more portable for other applications. Implemented by `event.py`.

**event.py** - This classfile defines the `Event`, the object abstraction for the events.

**test.py** - Test file for the various classes. Used during development to make sure everything was operating smoothly; feel free to run this file yourself to help check integrity.

**accounts.json** - Stores the account information. Interactions with this file are handled by the `User` abstraction. Of the form:

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
            "location": "Museum of Modern Art",
            "starttime": [
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
            "endtime": [
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
            "url": "http://www.moma.org/calendar/exhibitions/1553",
            "name": "Jackson Pollack Exhibit",
            "model": {
                "concepts": {
                    "Engraving": 0.74957967,
                    "Jackson Pollock": 0.84678906,
                    "Drawing": 0.7697984,
                    "Screen printing": 0.72784966,
                    "Painting": 0.70308614,
                    "1912": 0.33586192,
                    "United States": 0.37856802,
                    "Paper": 0.622553,
                    "Masterpiece": 0.644868,
                    "Paint": 0.58929,
                    "Figurative art": 0.8233745,
                    "Canvas": 0.75178367,
                    "Evolution": 0.5099157,
                    "Lithography": 0.7770813
                }
            },
            "description": "Long description...",
            "picture": ""
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

Write beautiful documentation.

Continue to populate an example list of events, using `curator.py`.

Stetch goal: Write `cleanup.py`.

Stretch goal: Write `emailer.py`.
