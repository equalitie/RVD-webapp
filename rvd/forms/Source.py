from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms_alchemy import ModelForm
from rvd.forms import organisation_factory
from rvd.models import Source


class SourceForm(ModelForm):

    class Meta:
        model = Source

    __order = ('name', 'organisations')

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

    organisations = QuerySelectMultipleField(query_factory=organisation_factory, get_label='name')
