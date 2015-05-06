from flask_babel import lazy_gettext as ___

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import fields, validators

from .. import models

class ProfessionForm(ModelForm):

    class Meta:
        model = models.Profession
   
    __order = ('name')

    def __iter__(self):
        f = list(super(ModelForm, self).__init__())
        gf = lambda fid: next((fld for fld in f if fld.id == fid))
        return (gf(fid) for fid in self.__order)
