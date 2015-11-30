from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required, Email

class StartForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    i1 = TextField('i1')
    i2 = TextField('i2')
    i3 = TextField('i3')
    i4 = TextField('i4')
    i5 = TextField('i5')
    i6 = TextField('i6')
    i7 = TextField('i7')
    i8 = TextField('i8')
    i9 = TextField('i9')
    i10 = TextField('i10')

class LoginForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])

class DashboardForm(Form):
    email = TextField('Email', validators=[Email()])
    password = PasswordField('Password')
    i1 = TextField('i1')
    i2 = TextField('i2')
    i3 = TextField('i3')
    i4 = TextField('i4')
    i5 = TextField('i5')