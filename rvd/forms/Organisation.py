from flask_babel import lazy_gettext as ___

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import fields, validators

from .. import models

class OrganisationForm(ModelForm):

    class Meta:
        model = models.Organisation
   
    __order = ('name', 'name', 'description', 'locations')

    def __iter__(self):
        f = list(super(ModelForm, self).__init__())
        gf = lambda fid: next((fld for fld in f if fld.id == fid))
        return (gf(fid) for fid in self.__order)
    
    locations = fields.SelectMultipleField(choices=[
        (str(i), l) for i, l in enumerate(['Russia', 'Canada', 'France', 'Germany'])])

