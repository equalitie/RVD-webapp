from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.Actor import ActorForm
from flask_admin import helpers
from collections import defaultdict
actors_bp = Blueprint('actors', __name__)

from ..models import Actor, Organisation, Location, Profession

@actors_bp.route('/actors/add', methods=('GET', 'POST'))
@login_required
def actors():
    actor_form = ActorForm(request.form)
    if helpers.validate_form_on_submit(actor_form):
        # the values are now accessible here
        actor_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})

        # Convert fields referring to other models into instances of those models
        organisations = request.form.getlist('organisations')
        test_org_loc = [Location(name='Test Location', longitude=44.0123, latitude=23.235)]
        organisations = [
          Organisation(name=actor_form.organisations.choices[i][1], description='test', locations=test_org_loc)
          for i in map(int, organisations)]
        actor_dict['organisations'] = organisations
        locations = request.form.getlist('locations')
        locations = [
            Location(name=actor_form.locations.choices[i][1], latitude=41.123, longitude=67.15)
            for i in map(int, locations)]
        actor_dict['locations'] = locations
        professions = request.form.getlist('professions')
        professions = [
            Profession(name=actor_form.professions.choices[i][1])
            for i in map(int, professions)]
        actor_dict['professions'] = professions

        # Convert the types of boolean fields
        actor_dict['gender'] = bool(actor_dict['gender'])
        actor_dict['is_activist'] = bool(actor_dict['is_activist'])

        # you probably want to do something like actor = Actor(**actor_dict)
        print actor_dict
        print 'Choices for organisations'
        actor_instance = Actor(**actor_dict)
        print 'Created actor with name ' + actor_instance.name
        # I made it defaultdict in case keys change, things like this won't break
        print actor_dict['123abd']

        return redirect('/actors/add?success=1')

    return render_template("actors.html", form=actor_form)
