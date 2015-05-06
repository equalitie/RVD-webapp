from flask_babel import lazy_gettext as ___

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import fields, validators

from .. import models

class ReleaseTypeForm(ModelForm):

    class Meta:
        model = models.ReleaseType
   
    __order = ('type_code')

    def __iter__(self):
        f = list(super(ModelForm, self).__init__())
        gf = lambda fid: next((fld for fld in f if fld.id == fid))
        return (gf(fid) for fid in self.__order)

