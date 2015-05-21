from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.Profession import ProfessionForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session
from rvd.models import Profession
from copy import copy
from rvd.views import flatten_instance
names = {
    'name': 'profession',
    'plural': 'professions',
    'slug': 'profession',
    'plural_slug': 'professions'
}
professions_bp = Blueprint('professions', __name__)


def gather_form_data():
    profession_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})
    profession_instance = Profession(**profession_dict)
    session.add(profession_instance)
    session.flush()

    return profession_instance


@professions_bp.route('/professions/add', methods=('GET', 'POST'))
@login_required
def professions():
    profession_form = ProfessionForm(request.form)
    if helpers.validate_form_on_submit(profession_form):
        profession_instance = gather_form_data()
        return redirect('/professions/{}?success=1'.format(profession_instance.id))
    data = copy(names)
    return render_template("item_edit.html", form=profession_form, action='add', data=data)


@professions_bp.route('/professions/<int:profession_id>')
@login_required
def view_profession(profession_id):
    profession = session.query(Profession).get(profession_id)
    fields = flatten_instance(profession, Profession)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@professions_bp.route('/professions/all')
@login_required
def view_all_professions():
    all_professions = session.query(Profession).all()
    all_professions = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_professions]
    data = copy(names)
    data['data'] = all_professions

    return render_template("item_view_all.html", data=data)


@professions_bp.route('/professions/<int:profession_id>/delete')
@login_required
def delete_profession(profession_id):
    profession = session.query(Profession).get(profession_id)
    session.delete(profession)
    session.flush()
    return redirect('/professions/all?success=1')


@professions_bp.route('/professions/<int:profession_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_profession(profession_id):
    profession = session.query(Profession).get(profession_id)
    profession_form = ProfessionForm(request.form, obj=profession)

    if helpers.validate_form_on_submit(profession_form):
        profession_form.populate_obj(profession)
        return redirect('/professions/{}?success=1'.format(profession_id))

    data = copy(names)
    data['data'] = profession

    return render_template("item_edit.html", data=data, form=profession_form, action='edit')