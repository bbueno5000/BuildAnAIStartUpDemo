import app
import flask
import flask_debugtoolbar

app = flask.Flask(__name__)
app.config.from_object('app.config')

db = flask.ext.sqlalchemy.SQLAlchemy(app)

mail = flask.ext.mail.Mail(app)

app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
toolbar = flask_debugtoolbar.DebugToolbarExtension(app)

bcrypt = flask.ext.bcrypt.Bcrypt(app)

app.register_blueprint(app.views.user.userbp)

login_manager = flask.ext.login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.signin'

@login_manager.user_loader
def load_user(email):
    """
    DOCSTRING
    """
    return app.models.User.query.filter(app.models.User.email == email).first()
