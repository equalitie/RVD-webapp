from wtforms_alchemy import ModelForm
from rvd.models import Prison
from rvd.forms import location_factory, prison_type_factory
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField


class PrisonForm(ModelForm):

    class Meta:
        model = Prison

    __order = ('name', 'locations', 'prison_types')

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

    locations = QuerySelectMultipleField(query_factory=location_factory, get_label='name')
    prison_types = QuerySelectMultipleField(query_factory=prison_type_factory, get_label='name')