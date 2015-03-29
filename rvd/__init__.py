"""
Everything we want available to the 'rvd' app module
"""
import os
from flask import Flask, redirect
from flask_login import LoginManager
from flask_babel import Babel
from lib.models.User import User

import config.check_config as check
from views.login import login_bp
from views.reports import reports_bp

# FLASK APP
static_paths = [os.getcwd(), '/lib/static']
app = Flask(__name__, instance_relative_config=True, static_folder="".join(static_paths))
app = check.check_config(app)

# BLUEPRINTS
app.register_blueprint(login_bp)
app.register_blueprint(reports_bp)

# LOCALIZED CONTENT
babel = Babel(app)

# Login ext for session management
login_manager = LoginManager()
login_manager.init_app(app)

# flask overrides


@login_manager.user_loader
def load_user(user_id):
    """
    Required for the login manager
    """
    user = User({"id": 0})
    return user


@app.errorhandler(401)
def custom_401(error):
    """
    User trying to access protected resources
    """
    return redirect("/")