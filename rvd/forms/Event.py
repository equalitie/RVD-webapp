from flask_babel import lazy_gettext as ___
from wtforms_alchemy import ModelForm
from wtforms import fields, validators
from rvd.models import Event
from rvd.forms import location_factory, release_type_factory, prison_factory, source_factory, witnesses_factory
from rvd.forms import victims_factory, perpetrators_factory, event_type_factory
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

display_func = lambda model: "{} ({}), {}".format(
    model.name, model.birth_date, ", ".join([x.name for x in model.organisations])
)


class EventForm(ModelForm):
    class Meta:
        model = Event

    __order = (
        'event_types', 'title', 'description', 'event_start', 'event_end', 'report_date',
        'charges', 'consequences', 'psych_assist', 'material_assist', 'was_activist',
        'victim_is_complainant', 'allow_storage', 'allow_publishing', 'allow_representation',
        'data_is_sensitive', 'locations', 'prisons', 'release_types', 'sources',
        'witnesses', 'victims', 'perpetrators', 'public'
    )

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

    # Use some example data for populating the form before we have some data to work with
    release_types = QuerySelectMultipleField(query_factory=release_type_factory, get_label='type_code')
    locations = QuerySelectMultipleField(query_factory=location_factory, get_label='name')
    prisons = QuerySelectMultipleField(query_factory=prison_factory, get_label='name')
    sources = QuerySelectMultipleField(query_factory=source_factory, get_label='name')
    witnesses = QuerySelectMultipleField(query_factory=witnesses_factory, get_label=display_func)
    victims = QuerySelectMultipleField(query_factory=victims_factory, get_label=display_func)
    perpetrators = QuerySelectMultipleField(query_factory=perpetrators_factory, get_label=display_func)
    event_types = QuerySelectMultipleField(query_factory=event_type_factory, get_label='name')

    psych_assist = fields.SelectField(___('Psychological assistance provided'),
                                      validators=[validators.required()],
                                      choices=[
                                          (1, ___('Yes')), (0, ___('No'))], coerce=bool)
    material_assist = fields.SelectField(___('Material assistance provided'),
                                         validators=[validators.required()],
                                         choices=[
                                             (1, ___('Yes')), (0, ___('No'))], coerce=bool)
    was_activist = fields.SelectField(___('Was an activist'),
                                      validators=[validators.required()],
                                      choices=[
                                          (1, ___('Yes')), (0, ___('No'))], coerce=bool)
    victim_is_complainant = fields.SelectField(___('Victim is complainant'),
                                               validators=[validators.required()],
                                               choices=[
                                                   (1, ___('Yes')), (0, ___('No'))], coerce=bool)
    allow_storage = fields.SelectField(___('Allows storage of information'),
                                       validators=[validators.required()],
                                       choices=[
                                           (1, ___('Yes')), (0, ___('No'))], coerce=bool)
    allow_publishing = fields.SelectField(___('Allows publishing of information'),
                                          validators=[validators.required()],
                                          choices=[
                                              (1, ___('Yes')), (0, ___('No'))], coerce=bool)
    allow_representation = fields.SelectField(___('Allows legal representation'),
                                              validators=[validators.required()],
                                              choices=[
                                                  (1, ___('Yes')), (0, ___('No'))], coerce=bool)
    data_is_sensitive = fields.SelectField(___('Data is hyper sensitive'),
                                           validators=[validators.required()],
                                           choices=[
                                               (1, ___('Yes')), (0, ___('No'))], coerce=bool)
    public = fields.SelectField(___('Public'), validators=[validators.required()], choices=[
        (1, ___('Yes')), (0, ___('No'))], coerce=bool)

    def validate_event_end(self, field):
        if field.data <= self.event_start.data:
            raise validators.ValidationError(___('End date has to be greater than start date.'))