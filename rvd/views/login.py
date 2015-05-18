from flask import Blueprint, render_template, request, redirect, make_response
from flask_login import login_required, current_user, login_user, logout_user
from flask_admin import helpers
from rvd.forms.Login import LoginForm
import logging
login_bp = Blueprint('login', __name__)


@login_bp.route('/', methods=('GET', 'POST'))
def login():
    login_form = LoginForm(request.form)

    # form is submitted and has been validated
    if helpers.validate_form_on_submit(login_form):
        try:
            login_user(login_form.user)
        except Exception as e:
            logging.error("Could not log in: %s", e)
            redirect('/')
        return redirect("/reports")

    return render_template('login.html', current_user=current_user, form=login_form)


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_bp.route('/lang')
@login_required
def language():
    cookie_lang = request.cookies.get('lang')
    return render_template("lang.html", locale=cookie_lang)


@login_bp.route('/lang/<lang>')
@login_required
def choose_language(lang):
    # check allowed languages
    allowed_langs = ["en", "fr", "es", "fa", "ru", "ma"]
    if lang in allowed_langs:
        # all looks good, return to where we came from
        resp = make_response(redirect("/lang"))
        resp.set_cookie('lang', lang)

        return resp
    return render_template("lang.html")
