import logging

ADMINS = ['flask.boilerplate@gmail.com']
ADMIN_CREDENTIALS = ('admin', 'pa$$word')
BCRYPT_LOG_ROUNDS = 12 # number of times a password is hashed
DEBUG = False # DEBUG has to be to False in a production environment for security reasons
LOG_BACKUPS = 2
LOG_FILENAME = 'activity.log'
LOG_LEVEL = logging.INFO
LOG_MAXBYTES = 1024
MAIL_PASSWORD = 'flaskboilerplate123'
MAIL_PORT = 465
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = 'flask.boilerplate'
SECRET_KEY = 'houdini'# secret key for generating tokens
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
