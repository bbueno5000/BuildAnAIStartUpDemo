"""
DOCSTRING
"""
import app
import flask.ext.login
import sqlalchemy.ext.hybrid

class User(app.db.Model, flask.ext.login.UserMixin):
    """
    A user who has an account on the website.
    """

    __tablename__ = 'users'
    _password = app.db.Column(app.db.String)
    confirmation = app.db.Column(app.db.Boolean)
    email = app.db.Column(app.db.String, primary_key=True)
    first_name = app.db.Column(app.db.String)
    last_name = app.db.Column(app.db.String)
    paid = app.db.Column(app.db.Boolean)
    phone = app.db.Column(app.db.String)

    def check_password(self, plaintext):
        return app.bcrypt.check_password_hash(self.password, plaintext)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_id(self):
        return self.email

    def is_paid(self):
        return self.paid

    @sqlalchemy.ext.hybrid.hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = app.bcrypt.generate_password_hash(plaintext)
