"""
DOCSTRING
"""
import app
import flask
import flask_admin
import os
import werkzeug.exceptions

admin = flask_admin.Admin(app.app, name='Admin', template_mode='bootstrap3')

class ModelView(flask.ext.admin.contrib.sqla.ModelView):
    """
    DOCSTRING
    """
    def is_accessible(self):
        """
        DOCSTRING
        """
        auth = flask.request.authorization or flask.request.environ.get('REMOTE_USER')
        if not auth or (auth.username, auth.password) != app.app.config['ADMIN_CREDENTIALS']:
            raise werkzeug.exceptions.HTTPException(
                '', flask.Response('You have to an administrator.', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}))
        return True

admin.add_view(ModelView(app.models.User, app.db.session))
path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(flask.ext.admin.contrib.fileadmin.FileAdmin(path, '/static/', name='Static'))
