from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.Source import SourceForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, Source
from rvd.forms import organisation_factory
from copy import copy
names = {
    'name': 'source',
    'plural': 'sources',
    'slug': 'source',
    'plural_slug': 'sources'
}
sources_bp = Blueprint('sources', __name__)


def get_name_from_id(needle, things):
    for thing in things:
        if int(thing.id) == int(needle):
            return thing


def gather_form_data():
    source_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})

    organisation = request.form.getlist('organisation')
    orgs = organisation_factory()
    source_dict['organisation'] = get_name_from_id(organisation[0], orgs)

    source_instance = Source(**source_dict)
    session.add(source_instance)
    session.commit()

    return source_instance


@sources_bp.route('/sources/add', methods=('GET', 'POST'))
@login_required
def sources():
    source_form = SourceForm(request.form)
    if helpers.validate_form_on_submit(source_form):
        source_instance = gather_form_data()
        return redirect('/sources/{}?success=1'.format(source_instance.id))

    data = copy(names)
    return render_template("item_edit.html", form=source_form, action='add', data=data)


def get_attr(a):
    if hasattr(a, 'name'):
        return a.name
    if hasattr(a, 'title'):
        return str(a.title)


def flatten_instance(obj):
    fields = {'id': obj.id}
    for c in obj.__table__.columns:
        fields[c.info.get('label')] = getattr(obj, c.key)
    from sqlalchemy.inspection import inspect

    for r in inspect(Source).relationships:
        associated_data = getattr(obj, r.key)
        fields[r.key] = ", ".join([get_attr(a) for a in associated_data]) if associated_data else None
    return fields


@sources_bp.route('/sources/<int:source_id>')
@login_required
def view_source(source_id):
    source = session.query(Source).get(source_id)
    fields = flatten_instance(source)
    data = copy(names)
    data['data'] = fields

    return render_template("item_view_single.html", data=data)


@sources_bp.route('/sources/all')
@login_required
def view_all_sources():
    all_sources = session.query(Source).all()
    all_sources = [{k: v for k, v in x.__dict__.iteritems() if not k.startswith('_sa_')} for x in all_sources]
    data = copy(names)
    data['data'] = all_sources

    return render_template("item_view_all.html", data=data)


@sources_bp.route('/sources/<int:source_id>/delete')
@login_required
def delete_source(source_id):
    source = session.query(Source).get(source_id)
    session.delete(source)
    session.commit()
    return redirect('/sources/all?success=1')


@sources_bp.route('/sources/<int:source_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_source(source_id):
    source = session.query(Source).get(source_id)
    source_form = SourceForm(request.form, obj=source)

    if helpers.validate_form_on_submit(source_form):
        source_form.populate_obj(source)
        return redirect('/sources/{}?success=1'.format(source_id))

    data = copy(names)
    data['data'] = source

    return render_template("item_edit.html", data=data, form=source_form, action='edit')