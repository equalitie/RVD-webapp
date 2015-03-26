import datetime
import os
import inspect


PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=24)
APP_FOLDER = os.path.dirname(
    os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
)

FRONTEND_HOST_IP = "127.0.0.1"
FRONTEND_PORT = 5000