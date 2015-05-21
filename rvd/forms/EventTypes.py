from wtforms_alchemy import ModelForm
from rvd.models import EventType


class EventTypesForm(ModelForm):

    class Meta:
        model = EventType