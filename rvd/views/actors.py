from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.Actor import ActorForm
from flask_admin import helpers
from collections import defaultdict
actors_bp = Blueprint('actors', __name__)


@actors_bp.route('/actors/add', methods=('GET', 'POST'))
@login_required
def actors():

    actor_form = ActorForm(request.form)

    actor_form.organisations.choices = [('{}'.format(x), 'Org {}'.format(x)) for x in xrange(10)]
    actor_form.location.choices = [('{}'.format(x), 'Org {}'.format(x)) for x in xrange(10)]
    actor_form.profession.choices = [('{}'.format(x), 'Org {}'.format(x)) for x in xrange(10)]

    if helpers.validate_form_on_submit(actor_form):
        # the values are now accessible here
        actor_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})
        # you probably want to do something like actor = Actor(**actor_dict)
        print actor_dict
        # I made it defaultdict in case keys change, things like this won't break
        print actor_dict['123abd']

        return redirect('/actors/add?success=1')

    return render_template("actors.html", form=actor_form)