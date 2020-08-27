"""
DOCSTRING
"""
import app
import flask.ext.mail
import threading

def send(recipient, subject, body):
    """
    Send a mail to a recipient. The body is usually a rendered HTML template.
    The sender's credentials has been configured in the config.py file.
    """
    sender = app.app.config['ADMINS'][0]
    message = flask.ext.mail.Message(subject, sender=sender, recipients=[recipient])
    message.html = body
    thr = threading.Thread(target=send_async, args=[app.app, message])
    thr.start()

def send_async(app, message):
    """
    Send the mail asynchronously.
    """
    with app.app.app_context():
        app.mail.send(message)
