"""
logger_setup.py customizes the app's logging module. Each time an event is
logged the logger checks the level of the event (eg. debug, warning, info...).
If the event is above the approved threshold then it goes through. The handlers
do the same thing; they output to a file/shell if the event level is above their
threshold.
:Example:
        >>> from website import logger
        >>> logger.info('event', foo='bar')
**Levels**:
        - logger.debug('For debugging purposes')
        - logger.info('An event occured, for example a database update')
        - logger.warning('Rare situation')
        - logger.error('Something went wrong')
        - logger.critical('Very very bad')
You can build a log incrementally as so:
        >>> log = logger.new(date='now')
        >>> log = log.bind(weather='rainy')
        >>> log.info('user logged in', user='John')
"""
import app
import datetime
import flask
import logging
import pytz
import structlog

app.app.logger.setLevel(app.app.config['LOG_LEVEL'])
app.app.logger.removeHandler(app.app.logger.handlers[0])
TZ = pytz.timezone(app.app.config['TIMEZONE'])

def add_fields(_, level, event_dict):
    """
    Add custom fields to each record.
    """
    now = datetime.datetime.now()
    event_dict['timestamp'] = TZ.localize(now, True).astimezone(pytz.utc).isoformat()
    event_dict['level'] = level
    if session:
        event_dict['session_id'] = flask.session.get('session_id')
    if request:
        try:
            event_dict['ip_address'] = \
                flask.request.headers['X-Forwarded-For'].split(',')[0].strip()
        except:
            event_dict['ip_address'] = 'unknown'
    return event_dict

if app.app.config.get('LOG_FILENAME'):
    file_handler = logging.handlers.RotatingFileHandler(
        filename=app.app.config['LOG_FILENAME'],
        maxBytes=app.app.config['LOG_MAXBYTES'],
        backupCount=app.app.config['LOG_BACKUPS'],
        mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    app.app.logger.addHandler(file_handler)

logger = structlog.wrap_logger(
    app.app.logger, processors=[
        add_fields, structlog.processors.JSONRenderer(indent=None)])
