from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from rvd.forms.Source import SourceForm
from flask_admin import helpers
from collections import defaultdict
from rvd.models import session, Source
from rvd.forms import organisation_factory
from copy import copy
from rvd.views import flatten_instance, get_name_from_id
names = {
    'name': 'source',
    'plural': 'sources',
    'slug': 'source',
    'plural_slug': 'sources'
}
sources_bp = Blueprint('sources', __name__)


def gather_form_data():
    source_dict = defaultdict(lambda: None, {value: field for value, field in request.form.iteritems()})

    organisation_ids = request.form.getlist('organisations')
    source_dict['organisations'] = [get_name_from_id(x, organisation_factory()) for x in organisation_ids]

    source_instance = Source(**source_dict)
    session.add(source_instance)
    session.flush()

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


@sources_bp.route('/sources/<int:source_id>')
@login_required
def view_source(source_id):
    source = session.query(Source).get(source_id)
    fields = flatten_instance(source, Source)
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
    session.flush()
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