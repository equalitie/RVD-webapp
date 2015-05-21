"""
Everything we want available to the 'rvd' app module
"""
import os
from flask import Flask, redirect, request, g
from flask_login import LoginManager
from flask_babel import Babel
from rvd.models import session, User

import config.check_config as check
from views.login import login_bp
from views.reports import reports_bp
from views.actors import actors_bp
from views.documents import documents_bp
from views.events import events_bp
from views.locations import locations_bp
from views.organisations import organisations_bp
from views.profession import professions_bp
from views.intl_authority import international_authority_bp
from views.prison_type import prison_types_bp
from views.prisons import prisons_bp
from views.release_types import release_types_bp
from views.event_types import event_types_bp
from views.sources import sources_bp
from views.state_authority import state_authority_bp
from views.events import events_bp
from views.evidence_type import evidence_types_bp
from views.users import users_bp
from models import session

import logging
import time

# FLASK APP
static_paths = [os.getcwd(), '/lib/static']
app = Flask(__name__, instance_relative_config=True, static_folder="".join(static_paths))
app = check.check_config(app)

# BLUEPRINTS
app.register_blueprint(login_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(actors_bp)
app.register_blueprint(documents_bp)
app.register_blueprint(events_bp)
app.register_blueprint(locations_bp)
app.register_blueprint(organisations_bp)
app.register_blueprint(professions_bp)
app.register_blueprint(international_authority_bp)
app.register_blueprint(prison_types_bp)
app.register_blueprint(prisons_bp)
app.register_blueprint(release_types_bp)
app.register_blueprint(event_types_bp)
app.register_blueprint(sources_bp)
app.register_blueprint(state_authority_bp)
app.register_blueprint(events_bp)
app.register_blueprint(evidence_types_bp)
app.register_blueprint(users_bp)

# LOCALIZED CONTENT
babel = Babel(app)

# Login ext for session management
login_manager = LoginManager()
login_manager.init_app(app)


# flask overrides
@app.before_request
def before_request():
    g.start = time.time()


@app.teardown_request
def teardown_request(exception=None):
    logging.info("Request took {} ms".format((time.time() - g.start)*1000))


@app.teardown_appcontext
def shutdown_session(exception=None):
    try:
        return session.commit()
    except Exception as e:
        logging.error(e.message)
    session.remove()


@login_manager.user_loader
def load_user(user_id):
    """
    Required for the login manager
    """
    user = session.query(User).get(user_id)
    return user


@app.errorhandler(401)
def custom_401(error):
    """
    User trying to access protected resources
    """
    return redirect("/")


@babel.localeselector
def get_locale():
    cookie_lang = request.cookies.get('lang')
    return cookie_lang if cookie_lang is not None else 'en'