"""
DOCSTRING
"""
import app.models
import flask.ext.wtf
import wtforms

class Forgot(flask.ext.wtf.Form):
    """
    User forgot password form.
    """
    email = wtforms.TextField(
        validators=[wtforms.validators.Required(), wtforms.validators.Email()],
        description='Email address')

class Login(flask.ext.wtf.Form):
    """
    User login form.
    """
    email = wtforms.TextField(
        validators=[wtforms.validators.Required(), wtforms.validators.Email()],
        description='Email address')
    password = wtforms.PasswordField(
        validators=[wtforms.validators.Required()], description='Password')

class Reset(flask.ext.wtf.Form):
    """
    User reset password form.
    """
    password = wtforms.PasswordField(
        validators=[
            wtforms.validators.Required(),
            wtforms.validators.Length(min=6),
            wtforms.validators.EqualTo('confirm', message='Passwords must match.')],
        description='Password')
    confirm = wtforms.PasswordField(description='Confirm password')

class SignUp(flask.ext.wtf.Form):
    """
    User sign up form.
    """
    first_name = wtforms.TextField(
        validators=[wtforms.validators.Required(), wtforms.validators.Length(min=2)],
        description='Name')
    last_name = wtforms.TextField(
        validators=[wtforms.validators.Required(), wtforms.validators.Length(min=2)],
        description='Surname')
    phone = wtforms.TextField(
        validators=[wtforms.validators.Required(), wtforms.validators.Length(min=6)],
        description='Phone number')
    email = wtforms.TextField(
        validators=[
            wtforms.validators.Required(),
            wtforms.validators.Email(),
            Unique(
                app.models.User,
                app.models.User.email,
                'This email address is already linked to an account.')],
        description='Email address')
    password = wtforms.PasswordField(
        validators=[
            wtforms.validators.Required(),
            wtforms.validators.Length(min=6),
            wtforms.validators.EqualTo('confirm', message='Passwords must match.')],
        description='Password')
    confirm = wtforms.PasswordField(description='Confirm password')

class Unique:
    """
    Custom validator to check an object's attribute is unique.
    For example, users should not be able to create an account,
    if the account's email address is already in the database.
    This class supposes you are using SQLAlchemy to query the database.
    """
    def __init__(self, model, field, message):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise wtforms.validators.ValidationError(self.message)
