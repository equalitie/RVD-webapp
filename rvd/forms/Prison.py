from flask_babel import lazy_gettext as ___

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import fields, validators

from .. import models

class PrisonForm(ModelForm):

    class Meta:
        model = models.Prison
   
    __order = ('name', 'locations', 'prison_types')

    def __iter__(self):
        f = list(super(ModelForm, self).__init__())
        gf = lambda fid: next((fld for fld in f if fld.id == fid))
        return (gf(fid) for fid in self.__order)
    
    locations = fields.SelectMultipleField(choices=[
        (str(i), l) for i, l in enumerate(['Cuba', 'Spain', 'Germany', 'United States'])])
    prison_types = fields.SelectMultipleField(choices=[
        (str(i), p) for i, p in enumerate(['Solitary', 'Torturing', 'Holding'])])

