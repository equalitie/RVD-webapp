from flask_babel import lazy_gettext as ___

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import fields, validators

from .. import models

class SourceForm(ModelForm):

    class Meta:
        model = models.Source

    __order = ('name', 'organisation')

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

    organisation = fields.SelectField(choices=[
        (str(i), o) for i, o in enumerate(['The Guardian', 'Propublica', 'The Intercept'])])
