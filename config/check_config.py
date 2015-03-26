import sys
import os


def check_server_env():
    if "SERVER_ENV" not in os.environ:
        print "Please make sure to set the SERVER_ENV environment variable before continuing. Value should be one of: "\
            "DEV, STAGING, PRODUCTION."
        sys.exit(1)
    print "Starting server in {} mode".format(os.environ["SERVER_ENV"])


def load_settings(app):
    app.config.from_object('config.default')
    app.config.from_pyfile('config.py')

    check_server_env()
    app.config["SERVER_ENV"] = os.environ["SERVER_ENV"]

    if app.config["SERVER_ENV"] == "STAGING":
        app.config.from_object('config.staging')
    elif app.config["SERVER_ENV"] == "PRODUCTION":
        app.config.from_object('config.production')

    return app


def check_config(app):
    app = load_settings(app)
    return app