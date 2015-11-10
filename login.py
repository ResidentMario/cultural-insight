# To implement Flask-Login in the code I need to make sense of these bits of code. This is not really a priority right now, though.
# If I wanted to take this to development stage this would be a priority!

from backend import authenticateUser, emailAlreadyInUse

################
# FLASK-LOGIN  #
# ##############
import flask.ext.login as flask_login

# Set up secret key.
# TODO: Obfuscate this by calling from a file.
app.secret_key = 'something really secret. well, not really, but eventually.'  # Change this!

# Initialize the login manager.

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if not emailAlreadyInUse(email):
        return
    else:
   		user = User()
		user.id = email
		return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if not authenticateUser(email):
        return
    else:
   		user = User()
		user.id = email
		# DO NOT ever store passwords in plaintext and always compare password
		# hashes using constant-time comparison!
		user.is_authenticated = request.form['password'] == users[email]['password']
		return user
###################
# END FLASK-LOGIN #
###################