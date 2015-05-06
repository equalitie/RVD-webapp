from flask_babel import lazy_gettext as ___

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import fields, validators

from .. import models

class RightsViolationForm(ModelForm):

    class Meta:
        model = models.RightsViolation

    __order = ('name', 'description', 'event')

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

    locations = fields.SelectMultipleField(choices=[
        ('0', "Montreal, QC"), ('1', "Toronto, ON"), ('2', "San Francisco, CA"), ('3', "Vancouver, BC")])
