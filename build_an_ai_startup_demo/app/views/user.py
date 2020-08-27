"""
DOCSTRING
"""
import app
import flask
import itsdangerous
import stripe

stripe_keys = {
    'secret_key': "sk_test_0VRS9K4LFsin7xx1cO1cBSip00W1BDqFRG",
    'publishable_key': "pk_test_TQmy1LFbeJ6tgZLOdzT4pZRh00mJ3yq97c"}

stripe.api_key = stripe_keys['secret_key']
# serializer for generating random tokens
ts = itsdangerous.URLSafeTimedSerializer(app.app.config['SECRET_KEY'])
# Create a user blueprint
userbp = flask.Blueprint('userbp', __name__, url_prefix='/user')

@userbp.route('/account')
@flask.ext.login.login_required
def account():
    """
    DOCSTRING
    """
    return flask.render_template('user/account.html', title='Account')

@app.app.route('/user/charge', methods=['POST'])
@flask.ext.login.login_required
def charge():
    """
    DOCSTRING
    """
    amount = 500
    customer = stripe.Customer.create(
        email=flask.ext.login.current_user.email,
        source=flask.request.form['stripeToken'])
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Service Plan')
    user = app.models.User.query.filter_by(
        email=flask.ext.login.current_user.email).first()
    user.paid = 1
    app.db.session.commit()
    return flask.render_template('user/charge.html', amount=amount)

@userbp.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm(token):
    """
    DOCSTRING
    """
    try:
        email = ts.loads(token, salt='email-confirm-key', max_age=86400)
    except:
        flask.abort(404)
    user = app.models.User.query.filter_by(email=email).first()
    user.confirmation = True
    app.db.session.commit()
    flask.flash('Your email address has been confirmed, you can sign in.', 'positive')
    return flask.redirect(flask.url_for('userbp.signin'))

@userbp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    """
    DOCSTRING
    """
    form = app.forms.user.Forgot()
    if form.validate_on_submit():
        user = app.models.User.query.filter_by(email=form.email.data).first()
        if user is not None:
            subject = 'Reset your password.'
            token = ts.dumps(user.email, salt='password-reset-key')
            resetUrl = flask.url_for('userbp.reset', token=token, _external=True)
            html = flask.render_template('email/reset.html', reset_url=resetUrl)
            email.send(user.email, subject, html)
            flask.flash('Check your emails to reset your password.', 'positive')
            return flask.redirect(flask.url_for('index'))
        else:
            flask.flash('Unknown email address.', 'negative')
            return flask.redirect(flask.url_for('userbp.forgot'))
    return flask.render_template('user/forgot.html', form=form)

@app.app.route('/user/pay')
@flask.ext.login.login_required
def pay():
    """
    DOCSTRING
    """
    user = app.models.User.query.filter_by(
        email=flask.ext.login.current_user.email).first()
    if user.paid == 0:
    	return flask.render_template(
            'user/buy.html', key=stripe_keys['publishable_key'],
            email=flask.ext.login.current_user.email)
    return "You already paid."

@app.app.route('/api/payFail', methods=['POST', 'GET'])
def payFail():
    """
    DOCSTRING
    """
    content = flask.request.json
    stripe_email = content['data']['object']['email']
    user = app.models.User.query.filter_by(email=stripe_email).first()
    if user is not None: 
        user.paid = 0
        app.db.session.commit()
    return 'Response: User with associated email {} updated (payment failure).'.format(str(stripe_email))

@app.app.route('/api/paySuccess', methods=['POST', 'GET'])
def paySuccess():
    """
    DOCSTRING
    """
    content = flask.request.json
    stripe_email = content['data']['object']['email']
    user = app.models.User.query.filter_by(email=stripe_email).first()
    if user is not None: 
        user.paid = 1
        app.db.session.commit()
    return 'Response: User with associated email {} updated (paid).'.format(str(stripe_email))

@userbp.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    """
    DOCSTRING
    """
    try:
        email = ts.loads(token, salt='password-reset-key', max_age=86400)
    except:
        flask.abort(404)
    form = app.forms.user.Reset()
    if form.validate_on_submit():
        user = app.models.User.query.filter_by(email=email).first()
        if user is not None:
            user.password = form.password.data
            app.db.session.commit()
            flask.flash('Your password has been reset, you can sign in.', 'positive')
            return flask.redirect(flask.url_for('userbp.signin'))
        else:
            flask.flash('Unknown email address.', 'negative')
            return flask.redirect(flask.url_for('userbp.forgot'))
    return render_template('user/reset.html', form=form, token=token)

@userbp.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    DOCSTRING
    """
    form = app.forms.user.Login()
    if form.validate_on_submit():
        user = app.models.User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                flask.ext.login.login_user(user)
                flask.flash('Succesfully signed in.', 'positive')
                return flask.redirect(flask.url_for('index'))
            else:
                flask.flash('The password you have entered is wrong.', 'negative')
                return flask.redirect(flask.url_for('userbp.signin'))
        else:
            flask.flash('Unknown email address.', 'negative')
            return flask.redirect(flask.url_for('userbp.signin'))
    return flask.render_template('user/signin.html', form=form, title='Sign in')

@userbp.route('/signout')
def signout():
    """
    DOCSTRING
    """
    flask.ext.login.logout_user()
    flask.flash('Succesfully signed out.', 'positive')
    return flask.redirect(flask.url_for('index'))

@userbp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    DOCSTRING
    """
    form = app.forms.user.SignUp()
    if form.validate_on_submit():
        user = app.models.User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            email=form.email.data,
            confirmation=False,
            password=form.password.data)
        app.db.session.add(user)
        app.db.session.commit()
        subject = 'Please confirm your email address.'
        token = ts.dumps(user.email, salt='email-confirm-key')
        confirmUrl = flask.url_for('userbp.confirm', token=token, _external=True)
        html = flask.render_template(
            'email/confirm.html', confirm_url=confirmUrl)
        app.toolbox.email.send(user.email, subject, html)
        flask.flash('Check your emails to confirm your email address.', 'positive')
        return flask.redirect(flask.url_for('index'))
    return flask.render_template('user/signup.html', form=form, title='Sign up')

